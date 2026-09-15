from celery import Celery

from backend.ai.models import AIRequest
from backend.audit.models import ActivityLog
from backend.auth.models import RefreshToken
from backend.automations.models import Automation, AutomationExecution
from backend.core.config import get_settings
from backend.customers.models import Customer
from backend.notifications.models import Notification
from backend.organizations.models import Membership, Organization
from backend.projects.models import Project
from backend.tasks.models import Task
from backend.users.models import User

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