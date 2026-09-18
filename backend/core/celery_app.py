from celery import Celery

from backend.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "nexora",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "run-all-automations-every-minute": {
        "task": "backend.automations.tasks.run_all_automations_task",
        "schedule": 60.0,
    },
}

celery_app.autodiscover_tasks(["backend.automations"])