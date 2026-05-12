from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "verifypk",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Karachi",
    enable_utc=True,
    task_track_started=True,
)
