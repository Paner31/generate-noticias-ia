from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class SearchRecency(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class PerplexitySearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of results")
    max_tokens: int = Field(default=1000, ge=100, le=4000, description="Max tokens per result")
    search_recency: Optional[SearchRecency] = Field(default=None, description="Time filter for results")
    country: Optional[str] = Field(default=None, description="Country code (e.g., 'US', 'MX')")
    search_after_date: Optional[str] = Field(default=None, description="Search after date (YYYY-MM-DD)")
    search_before_date: Optional[str] = Field(default=None, description="Search before date (YYYY-MM-DD)")
    domain_filter: Optional[List[str]] = Field(default=None, description="Filter by domains")
    language: Optional[str] = Field(default=None, description="Language code (e.g., 'en', 'es')")


class SearchResult(BaseModel):
    url: str
    title: str
    summary: str
    source: Optional[str] = None


class PerplexitySearchResponse(BaseModel):
    results: List[SearchResult]
    search_id: str
    total_results: int


class LinkGroup(BaseModel):
    group_id: str
    name: Optional[str] = None
    urls: List[str]


class GenerateNotesRequest(BaseModel):
    search_id: str
    selected_urls: List[str] = Field(..., description="Individual URLs to generate notes from")
    link_groups: List[LinkGroup] = Field(default=[], description="Grouped URLs for multi-source notes")
    custom_prompt: Optional[str] = Field(default=None, description="Custom prompt for note generation")
    max_tokens: int = Field(default=8000, ge=1000, le=16000)
    model: Optional[str] = Field(default=None, description="OpenRouter model to use")


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class GeneratedNote(BaseModel):
    note_id: str
    content: str
    sources: List[str]
    tokens_used: int
    model: str
    image_prompt: Optional[str] = Field(default="", description="AI image generation prompt")
    instagram_copy: Optional[str] = Field(default="", description="Instagram social media copy")
    facebook_copy: Optional[str] = Field(default="", description="Facebook social media copy")
    linkedin_copy: Optional[str] = Field(default="", description="LinkedIn social media copy")


class GenerateNotesResponse(BaseModel):
    notes: List[GeneratedNote] = Field(..., description="Generated notes")
    total_notes: int = Field(..., description="Total number of notes generated")
    message: str = Field(default="Notes generated successfully")
