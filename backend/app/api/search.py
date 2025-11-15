from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    PerplexitySearchRequest,
    PerplexitySearchResponse
)
from app.services.perplexity_service import PerplexityService
from app.core.session_storage import session_storage

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/", response_model=PerplexitySearchResponse)
async def search_news(search_request: PerplexitySearchRequest):
    """
    Perform a search using Perplexity API.

    Returns search results with URLs, titles, and summaries.
    Results are stored in session for later use in note generation.
    """
    try:
        perplexity = PerplexityService()
        result = await perplexity.search(search_request)

        # Store search results in session
        session_storage.store_search(
            search_id=result.search_id,
            search_request=search_request.model_dump(),
            results=[r.model_dump() for r in result.results]
        )

        return result

    except Exception as e:
        import traceback
        error_detail = f"Search failed: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)  # Log to console
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/{search_id}", response_model=PerplexitySearchResponse)
async def get_search_results(search_id: str):
    """
    Retrieve previously stored search results.
    """
    search_data = session_storage.get_search(search_id)

    if not search_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search not found"
        )

    return PerplexitySearchResponse(
        results=search_data["results"],
        search_id=search_data["search_id"],
        total_results=len(search_data["results"])
    )


@router.delete("/{search_id}")
async def delete_search(search_id: str):
    """
    Delete a search from session storage.
    """
    search_data = session_storage.get_search(search_id)

    if not search_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search not found"
        )

    session_storage.delete_search(search_id)

    return {"message": "Search deleted successfully"}
