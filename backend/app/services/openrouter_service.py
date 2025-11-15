import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings


class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # Optional, for rankings
            "X-Title": "News Generator"  # Optional, shows in rankings
        }

    async def generate_note(
        self,
        sources_content: List[Dict[str, str]],
        custom_prompt: Optional[str] = None,
        max_tokens: int = 8000,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a news article/note from multiple sources using OpenRouter.

        Args:
            sources_content: List of dicts with 'url' and 'content' keys
            custom_prompt: Optional custom instructions for note generation
            max_tokens: Maximum tokens for generation
            model: Model to use (defaults to settings)

        Returns:
            Dict with 'content' and 'tokens_used'
        """
        # Build the context from sources
        context = self._build_context(sources_content)

        # Build the system prompt
        system_prompt = self._build_system_prompt(custom_prompt)

        # Build the user message
        user_message = f"""Generate a comprehensive news article based on the following sources:

{context}

Instructions:
- Write a well-structured, journalistic article
- Combine information from all sources
- Maintain objectivity and accuracy
- Include relevant quotes if available
- Cite sources naturally in the text
- Aim for a professional, engaging tone
"""

        payload = {
            "model": model or settings.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                # Extract generated content
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                tokens_used = data.get("usage", {}).get("total_tokens", 0)

                return {
                    "content": content,
                    "tokens_used": tokens_used,
                    "model": model or settings.OPENROUTER_MODEL
                }

            except httpx.HTTPError as e:
                raise Exception(f"OpenRouter API error: {str(e)}")

    def _build_context(self, sources_content: List[Dict[str, str]]) -> str:
        """Build formatted context from sources."""
        context_parts = []

        for i, source in enumerate(sources_content, 1):
            url = source.get("url", "Unknown source")
            content = source.get("content", "")
            title = source.get("title", f"Source {i}")

            context_parts.append(f"""
Source {i}: {title}
URL: {url}
---
{content}
---
""")

        return "\n\n".join(context_parts)

    def _build_system_prompt(self, custom_prompt: Optional[str] = None) -> str:
        """Build the system prompt for note generation."""
        base_prompt = """You are a professional journalist and news writer. Your task is to create well-researched, accurate, and engaging news articles based on multiple sources.

Key guidelines:
- Maintain journalistic integrity and objectivity
- Synthesize information from multiple sources
- Write in a clear, professional style
- Structure articles with: headline-worthy opening, key facts, context, and conclusion
- Attribute information to sources when relevant
- Avoid speculation or unverified claims
"""

        if custom_prompt:
            return f"{base_prompt}\n\nAdditional instructions from user:\n{custom_prompt}"

        return base_prompt

    async def test_connection(self) -> bool:
        """Test if OpenRouter API is accessible."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self.headers
                )
                response.raise_for_status()
                return True
            except:
                return False
