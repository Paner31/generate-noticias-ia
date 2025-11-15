from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    PERPLEXITY_API_KEY: str
    OPENROUTER_API_KEY: str

    # Redis Configuration
    REDIS_URL: str

    # Server Configuration
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"

    # Generation Limits
    MAX_NOTES_PER_GENERATION: int = 5
    DEFAULT_MAX_TOKENS: int = 8000

    # OpenRouter Configuration
    OPENROUTER_MODEL: str = "z-ai/glm-4.6"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
