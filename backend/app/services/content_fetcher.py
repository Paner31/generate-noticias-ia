import httpx
from typing import Dict, Optional
import asyncio


class ContentFetcher:
    """Service to fetch full content from URLs using Jina Reader."""

    def __init__(self):
        self.jina_base_url = "https://r.jina.ai/"
        self.timeout = 30.0

    async def fetch_content(self, url: str) -> Optional[str]:
        """
        Fetch full content from a URL using Jina Reader.

        Args:
            url: The URL to fetch content from

        Returns:
            Full content as markdown string, or None if failed
        """
        try:
            # Jina Reader converts any webpage to clean markdown
            jina_url = f"{self.jina_base_url}{url}"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(jina_url)
                response.raise_for_status()

                # Jina returns clean markdown content
                content = response.text

                # Limit content length to avoid token issues (max ~10k words)
                max_chars = 50000
                if len(content) > max_chars:
                    content = content[:max_chars] + "\n\n[Content truncated due to length]"

                return content

        except httpx.HTTPError as e:
            print(f"[WARNING] Failed to fetch content from {url}: {str(e)}")
            return None
        except Exception as e:
            print(f"[WARNING] Unexpected error fetching {url}: {str(e)}")
            return None

    async def fetch_multiple(self, urls: list[str]) -> Dict[str, Optional[str]]:
        """
        Fetch content from multiple URLs concurrently.

        Args:
            urls: List of URLs to fetch

        Returns:
            Dictionary mapping URL to content (or None if failed)
        """
        tasks = [self.fetch_content(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(zip(urls, results))
