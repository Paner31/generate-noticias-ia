from celery import Task
from app.core.celery_app import celery_app
from app.services.perplexity_service import PerplexityService
from app.services.openrouter_service import OpenRouterService
from app.services.content_fetcher import ContentFetcher
from typing import List, Dict, Any
import uuid
import asyncio
from datetime import datetime
import redis
import json
from app.core.config import settings

# Redis client for shared storage between processes
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=10,  # 10 seconds timeout for operations
    socket_connect_timeout=10,  # 10 seconds timeout for connection
    socket_keepalive=True,
    retry_on_timeout=True,
    health_check_interval=30
)


def _save_job_to_redis(job_id: str, job_data: Dict[str, Any]):
    """Save job data to Redis with retry logic."""
    # Convert datetime objects to ISO string for JSON serialization
    job_data_copy = job_data.copy()
    if job_data_copy.get("created_at"):
        job_data_copy["created_at"] = job_data_copy["created_at"].isoformat()
    if job_data_copy.get("completed_at"):
        job_data_copy["completed_at"] = job_data_copy["completed_at"].isoformat()

    redis_key = f"job:{job_id}"

    # Retry logic for Redis operations
    max_retries = 3
    for attempt in range(max_retries):
        try:
            redis_client.setex(
                redis_key,
                3600,  # Expire after 1 hour
                json.dumps(job_data_copy)
            )
            print(f"[DEBUG] Saved to Redis key: {redis_key}, status: {job_data.get('status')}")
            return
        except (redis.exceptions.TimeoutError, redis.exceptions.ConnectionError) as e:
            if attempt < max_retries - 1:
                print(f"[WARNING] Redis timeout on attempt {attempt + 1}, retrying...")
                import time
                time.sleep(0.5)  # Wait 500ms before retry
            else:
                print(f"[ERROR] Failed to save to Redis after {max_retries} attempts: {e}")
                raise


def _get_job_from_redis(job_id: str) -> Dict[str, Any] | None:
    """Get job data from Redis with retry logic."""
    redis_key = f"job:{job_id}"

    # Retry logic for Redis operations
    max_retries = 3
    for attempt in range(max_retries):
        try:
            data = redis_client.get(redis_key)
            print(f"[DEBUG] Get from Redis key: {redis_key}, found: {data is not None}")
            if data:
                job_data = json.loads(data)
                # Convert ISO strings back to datetime
                if job_data.get("created_at"):
                    job_data["created_at"] = datetime.fromisoformat(job_data["created_at"])
                if job_data.get("completed_at"):
                    job_data["completed_at"] = datetime.fromisoformat(job_data["completed_at"])
                return job_data
            return None
        except (redis.exceptions.TimeoutError, redis.exceptions.ConnectionError) as e:
            if attempt < max_retries - 1:
                print(f"[WARNING] Redis timeout on attempt {attempt + 1}, retrying...")
                import time
                time.sleep(0.5)  # Wait 500ms before retry
            else:
                print(f"[ERROR] Failed to get from Redis after {max_retries} attempts: {e}")
                return None  # Return None instead of raising to avoid breaking the API


class GenerateNotesTask(Task):
    """Custom task class for note generation."""
    name = "app.core.tasks.generate_notes"

    def run(self, job_id: str, search_results: List[Dict], selected_urls: List[str],
            link_groups: List[Dict], custom_prompt: str = None, max_tokens: int = 8000,
            model: str = None) -> Dict[str, Any]:
        """
        Generate notes from selected sources.

        Args:
            job_id: Unique job identifier
            search_results: Original search results from Perplexity
            selected_urls: Individual URLs selected by user
            link_groups: Groups of URLs for multi-source notes
            custom_prompt: Custom prompt for generation
            max_tokens: Max tokens per note
            model: OpenRouter model to use
        """
        # Update job status
        job_data = {
            "job_id": job_id,
            "status": "processing",
            "progress": 0,
            "notes": [],
            "error": None,
            "created_at": datetime.utcnow(),
            "completed_at": None
        }
        _save_job_to_redis(job_id, job_data)

        try:
            # Run async generation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self._generate_notes_async(
                    job_id, search_results, selected_urls, link_groups,
                    custom_prompt, max_tokens, model
                )
            )
            loop.close()

            return result

        except Exception as e:
            job_data = _get_job_from_redis(job_id)
            if job_data:
                job_data["status"] = "failed"
                job_data["error"] = str(e)
                job_data["completed_at"] = datetime.utcnow()
                _save_job_to_redis(job_id, job_data)
            raise

    async def _generate_notes_async(
        self, job_id: str, search_results: List[Dict], selected_urls: List[str],
        link_groups: List[Dict], custom_prompt: str, max_tokens: int, model: str
    ) -> Dict[str, Any]:
        """Async method to generate notes."""
        openrouter = OpenRouterService()
        content_fetcher = ContentFetcher()
        generated_notes = []

        # Calculate total tasks
        total_tasks = len(selected_urls) + len(link_groups)

        if total_tasks == 0:
            raise ValueError("No URLs or groups selected")

        if total_tasks > 5:
            raise ValueError(f"Maximum 5 notes allowed, got {total_tasks}")

        # Collect all unique URLs
        all_urls = set(selected_urls)
        for group in link_groups:
            all_urls.update(group.get("urls", []))

        # Fetch full content for all URLs concurrently
        print(f"[INFO] Fetching full content for {len(all_urls)} URLs...")
        url_contents = await content_fetcher.fetch_multiple(list(all_urls))
        print(f"[INFO] Successfully fetched content for {sum(1 for c in url_contents.values() if c)} URLs")

        current_task = 0

        # Process individual URLs
        for url in selected_urls:
            # Get full content from Jina Reader
            full_content = url_contents.get(url)

            # Fallback to Perplexity summary if Jina failed
            if not full_content:
                print(f"[WARNING] Using Perplexity summary for {url} (full content fetch failed)")
                source_data = self._find_source_data(url, search_results)
                if source_data:
                    full_content = source_data.get("content", "")

            if full_content:
                # Get metadata from search results
                source_metadata = self._find_source_data(url, search_results) or {}

                source_data = {
                    "url": url,
                    "title": source_metadata.get("title", "Article"),
                    "content": full_content
                }

                # Generate note
                note = await openrouter.generate_note(
                    sources_content=[source_data],
                    custom_prompt=custom_prompt,
                    max_tokens=max_tokens,
                    model=model
                )

                generated_notes.append({
                    "note_id": str(uuid.uuid4()),
                    "content": note["content"],
                    "sources": [url],
                    "tokens_used": note["tokens_used"],
                    "model": note["model"]
                })

            current_task += 1
            progress = int((current_task / total_tasks) * 100)
            job_data = _get_job_from_redis(job_id)
            if job_data:
                job_data["progress"] = progress
                job_data["notes"] = generated_notes
                _save_job_to_redis(job_id, job_data)

        # Process link groups
        for group in link_groups:
            group_urls = group.get("urls", [])
            sources_data = []

            # Collect all sources for this group with full content
            for url in group_urls:
                # Get full content from Jina Reader
                full_content = url_contents.get(url)

                # Fallback to Perplexity summary if Jina failed
                if not full_content:
                    print(f"[WARNING] Using Perplexity summary for {url} (full content fetch failed)")
                    source_metadata = self._find_source_data(url, search_results)
                    if source_metadata:
                        full_content = source_metadata.get("content", "")

                if full_content:
                    # Get metadata from search results
                    source_metadata = self._find_source_data(url, search_results) or {}

                    sources_data.append({
                        "url": url,
                        "title": source_metadata.get("title", "Article"),
                        "content": full_content
                    })

            if sources_data:
                # Generate note from multiple sources
                note = await openrouter.generate_note(
                    sources_content=sources_data,
                    custom_prompt=custom_prompt,
                    max_tokens=max_tokens,
                    model=model
                )

                generated_notes.append({
                    "note_id": str(uuid.uuid4()),
                    "content": note["content"],
                    "sources": group_urls,
                    "tokens_used": note["tokens_used"],
                    "model": note["model"]
                })

            current_task += 1
            progress = int((current_task / total_tasks) * 100)
            job_data = _get_job_from_redis(job_id)
            if job_data:
                job_data["progress"] = progress
                job_data["notes"] = generated_notes
                _save_job_to_redis(job_id, job_data)

        # Mark job as completed
        job_data = _get_job_from_redis(job_id)
        if job_data:
            job_data["status"] = "completed"
            job_data["progress"] = 100
            job_data["completed_at"] = datetime.utcnow()
            _save_job_to_redis(job_id, job_data)
            return job_data
        return None

    def _find_source_data(self, url: str, search_results: List[Dict]) -> Dict[str, str]:
        """Find source data from search results."""
        for result in search_results:
            if result.get("url") == url:
                return {
                    "url": result.get("url"),
                    "title": result.get("title"),
                    "content": result.get("summary")
                }
        return None


# Register the task
generate_notes_task = celery_app.register_task(GenerateNotesTask())


def get_job_status(job_id: str) -> Dict[str, Any] | None:
    """Get the status of a job from Redis."""
    return _get_job_from_redis(job_id)
