from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "workout_tracker",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    include=[
        "app.tasks.reminders",
        "app.tasks.schedule_checker",
    ],
)


celery_app.conf.beat_schedule = {
    "check_workout_schedules_every_minute": {
        "task": "app.tasks.schedule_checker.check_workout_schedules",
        "schedule": crontab(minute="*"),
    },
}

celery_app.conf.timezone = "UTC"
