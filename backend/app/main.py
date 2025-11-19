from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import search, generate
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="News Generator API",
    description="API for generating news articles from web searches",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router)
app.include_router(generate.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "News Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "api": "running"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=True
    )
