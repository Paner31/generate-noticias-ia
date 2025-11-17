from typing import List, Dict, Any
import uuid
from app.services.openrouter_service import OpenRouterService
from app.services.content_fetcher import ContentFetcher


class NoteGeneratorService:
    """Service for generating news notes from sources."""

    def __init__(self):
        self.openrouter = OpenRouterService()
        self.content_fetcher = ContentFetcher()

    async def generate_notes(
        self,
        search_results: List[Dict],
        selected_urls: List[str],
        link_groups: List[Dict],
        custom_prompt: str = None,
        max_tokens: int = 8000,
        model: str = None
    ) -> List[Dict[str, Any]]:
        """
        Generate notes from selected sources.

        Args:
            search_results: Original search results from Perplexity
            selected_urls: Individual URLs selected by user
            link_groups: Groups of URLs for multi-source notes
            custom_prompt: Custom prompt for generation
            max_tokens: Max tokens per note
            model: OpenRouter model to use

        Returns:
            List of generated notes with content and metadata
        """
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
        url_contents = await self.content_fetcher.fetch_multiple(list(all_urls))
        print(f"[INFO] Successfully fetched content for {sum(1 for c in url_contents.values() if c)} URLs")

        # Process individual URLs
        for url in selected_urls:
            print(f"[INFO] Generating note for URL: {url}")

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
                note = await self.openrouter.generate_note(
                    sources_content=[source_data],
                    custom_prompt=custom_prompt,
                    max_tokens=max_tokens,
                    model=model
                )

                # Generate image content based on the note
                image_content = await self.openrouter.generate_image_content(
                    article_content=note["content"],
                    model=model
                )

                generated_notes.append({
                    "note_id": str(uuid.uuid4()),
                    "content": note["content"],
                    "sources": [url],
                    "tokens_used": note["tokens_used"] + image_content.get("tokens_used", 0),
                    "model": note["model"],
                    "image_prompt": image_content.get("image_prompt", ""),
                    "instagram_copy": image_content.get("instagram_copy", ""),
                    "facebook_copy": image_content.get("facebook_copy", ""),
                    "linkedin_copy": image_content.get("linkedin_copy", "")
                })

        # Process link groups
        for group in link_groups:
            group_urls = group.get("urls", [])
            print(f"[INFO] Generating note for group with {len(group_urls)} URLs")

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
                note = await self.openrouter.generate_note(
                    sources_content=sources_data,
                    custom_prompt=custom_prompt,
                    max_tokens=max_tokens,
                    model=model
                )

                # Generate image content based on the note
                image_content = await self.openrouter.generate_image_content(
                    article_content=note["content"],
                    model=model
                )

                generated_notes.append({
                    "note_id": str(uuid.uuid4()),
                    "content": note["content"],
                    "sources": group_urls,
                    "tokens_used": note["tokens_used"] + image_content.get("tokens_used", 0),
                    "model": note["model"],
                    "image_prompt": image_content.get("image_prompt", ""),
                    "instagram_copy": image_content.get("instagram_copy", ""),
                    "facebook_copy": image_content.get("facebook_copy", ""),
                    "linkedin_copy": image_content.get("linkedin_copy", "")
                })

        print(f"[INFO] Successfully generated {len(generated_notes)} notes")
        return generated_notes

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
