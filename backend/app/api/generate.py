from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    GenerateNotesRequest,
    GenerateNotesResponse,
    JobStatusResponse,
    JobStatus
)
from app.core.tasks import generate_notes_task, get_job_status, _save_job_to_redis
from app.core.session_storage import session_storage
from app.core.config import settings
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/generate", tags=["generate"])


@router.post("/", response_model=GenerateNotesResponse)
async def generate_notes(request: GenerateNotesRequest):
    """
    Generate news notes from selected URLs and groups.

    Creates a background job that processes the selected sources
    and generates articles using OpenRouter.

    Returns a job_id that can be used to track progress.
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

    # Create job
    job_id = str(uuid.uuid4())

    # Initialize job in Redis BEFORE sending to Celery
    initial_job_data = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0,
        "notes": [],
        "error": None,
        "created_at": datetime.utcnow(),
        "completed_at": None
    }
    _save_job_to_redis(job_id, initial_job_data)
    print(f"[DEBUG] Saved initial job to Redis: {job_id}")

    # Start background task
    try:
        generate_notes_task.apply_async(
            kwargs={
                "job_id": job_id,
                "search_results": search_data["results"],
                "selected_urls": request.selected_urls,
                "link_groups": [g.model_dump() for g in request.link_groups],
                "custom_prompt": request.custom_prompt,
                "max_tokens": request.max_tokens,
                "model": request.model
            },
            task_id=job_id
        )

        return GenerateNotesResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            message="Note generation started. Use the job_id to check status."
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start generation: {str(e)}"
        )


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_generation_status(job_id: str):
    """
    Get the status of a note generation job.

    Returns current progress, generated notes (if any), and errors.
    """
    print(f"[DEBUG] Querying job status for: {job_id}")
    job_data = get_job_status(job_id)
    print(f"[DEBUG] Job data retrieved: {job_data is not None}")

    if not job_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return JobStatusResponse(
        job_id=job_data["job_id"],
        status=job_data["status"],
        progress=job_data["progress"],
        notes=job_data["notes"],
        error=job_data.get("error"),
        created_at=job_data["created_at"],
        completed_at=job_data.get("completed_at")
    )
