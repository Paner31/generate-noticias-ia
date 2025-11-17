from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    GenerateNotesRequest,
    GenerateNotesResponse,
    GeneratedNote
)
from app.core.session_storage import session_storage
from app.core.config import settings
from app.services.note_generator import NoteGeneratorService

router = APIRouter(prefix="/api/generate", tags=["generate"])


@router.post("/", response_model=GenerateNotesResponse)
async def generate_notes(request: GenerateNotesRequest):
    """
    Generate news notes from selected URLs and groups.

    Processes the selected sources and generates articles using OpenRouter.
    Returns the generated notes directly.
    """
    # Validate search exists
    search_data = session_storage.get_search(request.search_id)
    if not search_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search not found. Please perform a search first."
        )

    # Validate total notes count
    total_notes = len(request.selected_urls) + len(request.link_groups)
    if total_notes == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No URLs or groups selected"
        )

    if total_notes > settings.MAX_NOTES_PER_GENERATION:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {settings.MAX_NOTES_PER_GENERATION} notes allowed per generation"
        )

    # Validate all URLs exist in search results
    search_urls = {result["url"] for result in search_data["results"]}

    for url in request.selected_urls:
        if url not in search_urls:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"URL not found in search results: {url}"
            )

    for group in request.link_groups:
        for url in group.urls:
            if url not in search_urls:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"URL not found in search results: {url}"
                )

    # Generate notes
    try:
        generator = NoteGeneratorService()
        notes = await generator.generate_notes(
            search_results=search_data["results"],
            selected_urls=request.selected_urls,
            link_groups=[g.model_dump() for g in request.link_groups],
            custom_prompt=request.custom_prompt,
            max_tokens=request.max_tokens,
            model=request.model
        )

        return GenerateNotesResponse(
            notes=[GeneratedNote(**note) for note in notes],
            total_notes=len(notes),
            message=f"Successfully generated {len(notes)} note(s)"
        )

    except Exception as e:
        print(f"[ERROR] Failed to generate notes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate notes: {str(e)}"
        )
