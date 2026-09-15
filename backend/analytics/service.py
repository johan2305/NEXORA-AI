import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.ai.models import AIRequest
from backend.automations.models import Automation, AutomationExecution
from backend.customers.models import Customer
from backend.projects.models import Project
from backend.tasks.models import Task


def get_summary(db: Session, organization_id: uuid.UUID) -> dict:
    tasks_query = db.query(Task).filter(
        Task.organization_id == organization_id, Task.deleted_at.is_(None)
    )
    total_tasks = tasks_query.count()

    tasks_by_status = dict(
        db.query(Task.status, func.count(Task.id))
        .filter(Task.organization_id == organization_id, Task.deleted_at.is_(None))
        .group_by(Task.status)
        .all()
    )

    tasks_by_created_by = dict(
        db.query(Task.created_by, func.count(Task.id))
        .filter(Task.organization_id == organization_id, Task.deleted_at.is_(None))
        .group_by(Task.created_by)
        .all()
    )

    total_customers = (
        db.query(Customer)
        .filter(Customer.organization_id == organization_id, Customer.deleted_at.is_(None))
        .count()
    )

    total_projects = (
        db.query(Project)
        .filter(Project.organization_id == organization_id, Project.deleted_at.is_(None))
        .count()
    )

    total_automations = (
        db.query(Automation).filter(Automation.organization_id == organization_id).count()
    )

    automation_executions_success = (
        db.query(AutomationExecution)
        .filter(
            AutomationExecution.organization_id == organization_id,
            AutomationExecution.status == "success",
        )
        .count()
    )

    automation_executions_failed = (
        db.query(AutomationExecution)
        .filter(
            AutomationExecution.organization_id == organization_id,
            AutomationExecution.status == "failed",
        )
        .count()
    )

    ai_requests_total = (
        db.query(AIRequest).filter(AIRequest.organization_id == organization_id).count()
    )

    ai_avg_latency = (
        db.query(func.avg(AIRequest.latency_ms))
        .filter(AIRequest.organization_id == organization_id)
        .scalar()
    )

    tasks_automated = tasks_by_created_by.get("automation", 0) + tasks_by_created_by.get("ai", 0)
    estimated_hours_saved = round(tasks_automated * 0.25, 1)

    return {
        "total_tasks": total_tasks,
        "tasks_by_status": tasks_by_status,
        "tasks_by_created_by": tasks_by_created_by,
        "total_customers": total_customers,
        "total_projects": total_projects,
        "total_automations": total_automations,
        "automation_executions_success": automation_executions_success,
        "automation_executions_failed": automation_executions_failed,
        "ai_requests_total": ai_requests_total,
        "ai_avg_latency_ms": round(ai_avg_latency, 1) if ai_avg_latency else None,
        "estimated_hours_saved": estimated_hours_saved,
    }