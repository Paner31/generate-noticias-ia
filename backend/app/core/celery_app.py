from celery import Celery
from app.core.config import settings

# Initialize Celery app
celery_app = Celery(
    "news_generator",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes max per task
    task_soft_time_limit=540,  # 9 minutes soft limit
    result_expires=3600,  # Results expire after 1 hour
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.core"])
