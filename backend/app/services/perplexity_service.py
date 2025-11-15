import httpx
from typing import List, Dict, Any, Optional
from app.models.schemas import PerplexitySearchRequest, SearchResult, PerplexitySearchResponse
from app.core.config import settings
import uuid


class PerplexityService:
    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def search(self, search_request: PerplexitySearchRequest) -> PerplexitySearchResponse:
        """
        Perform search using Perplexity API.
        Returns search results with URLs, titles, and summaries.
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Build the search message
            search_message = self._build_search_message(search_request)

            payload = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful search assistant. Provide concise summaries of web search results with their sources."
                    },
                    {
                        "role": "user",
                        "content": search_message
                    }
                ],
                "max_tokens": search_request.max_tokens,
                "temperature": 0.2,
                "top_p": 0.9,
                "return_citations": True,
                "search_domain_filter": search_request.domain_filter or [],
                "return_images": False,
                "return_related_questions": False,
                "search_recency_filter": search_request.search_recency.value if search_request.search_recency else None,
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1
            }

            # Add date filters if provided
            if search_request.search_after_date:
                payload["search_after_date"] = search_request.search_after_date
            if search_request.search_before_date:
                payload["search_before_date"] = search_request.search_before_date

            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                # Parse results from Perplexity response
                results = self._parse_perplexity_response(data, search_request.max_results)
                search_id = str(uuid.uuid4())

                return PerplexitySearchResponse(
                    results=results,
                    search_id=search_id,
                    total_results=len(results)
                )

            except httpx.HTTPError as e:
                error_detail = str(e)
                try:
                    if hasattr(e, 'response') and e.response is not None:
                        error_detail = f"{str(e)} - Response: {e.response.text}"
                except:
                    pass
                raise Exception(f"Perplexity API error: {error_detail}")

    def _build_search_message(self, search_request: PerplexitySearchRequest) -> str:
        """Build the search query message with filters."""
        message = f"Search for: {search_request.query}\n\n"
        message += f"Please provide up to {search_request.max_results} relevant web search results. "
        message += "For each result, include:\n"
        message += "1. The exact URL/source\n"
        message += "2. A clear title\n"
        message += "3. A concise summary of the content\n\n"

        if search_request.language:
            message += f"Language preference: {search_request.language}\n"
        if search_request.country:
            message += f"Country focus: {search_request.country}\n"

        return message

    def _parse_perplexity_response(self, data: Dict[str, Any], max_results: int) -> List[SearchResult]:
        """
        Parse Perplexity API response and extract search results.
        Perplexity returns citations which contain URLs and snippets.
        """
        results = []

        # Get the main content
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        # Get citations (sources)
        citations = data.get("citations", [])

        # If we have citations, use them
        if citations:
            for i, url in enumerate(citations[:max_results]):
                # Try to extract title and summary from content
                # This is a simplified approach - you may want to enhance this
                results.append(SearchResult(
                    url=url,
                    title=f"Source {i+1}",
                    summary=self._extract_summary_for_url(content, url, i),
                    source=self._extract_domain(url)
                ))
        else:
            # Fallback: parse content for URLs if no citations
            results = self._fallback_parse_content(content, max_results)

        return results

    def _extract_summary_for_url(self, content: str, url: str, index: int) -> str:
        """Extract relevant summary for a given URL from the content."""
        # Split content into paragraphs
        paragraphs = content.split('\n\n')

        # Try to find paragraph mentioning this source
        for para in paragraphs:
            if f"[{index+1}]" in para or url in para:
                # Clean up the paragraph
                clean_para = para.replace(f"[{index+1}]", "").strip()
                if len(clean_para) > 50:
                    return clean_para[:300] + "..." if len(clean_para) > 300 else clean_para

        # Fallback: return first paragraph or generic message
        if paragraphs and len(paragraphs[0]) > 50:
            return paragraphs[0][:300] + "..." if len(paragraphs[0]) > 300 else paragraphs[0]

        return "Relevant information found for your search query."

    def _fallback_parse_content(self, content: str, max_results: int) -> List[SearchResult]:
        """Fallback method to parse content when no citations are available."""
        results = []
        lines = content.split('\n')

        for i, line in enumerate(lines[:max_results]):
            if line.strip():
                results.append(SearchResult(
                    url=f"https://example.com/result-{i+1}",
                    title=f"Result {i+1}",
                    summary=line.strip()[:300],
                    source="unknown"
                ))

        return results

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return "unknown"
