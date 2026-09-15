import uuid
from datetime import datetime, timezone

from sqlalchemy import not_, select
from sqlalchemy.orm import Session

from backend.automations.models import Automation, AutomationExecution
from backend.customers.models import Customer
from backend.tasks.models import Task


def create(db: Session, organization_id: uuid.UUID, data: dict) -> Automation:
    automation = Automation(organization_id=organization_id, **data)
    db.add(automation)
    db.flush()
    return automation


def get_by_id(db: Session, organization_id: uuid.UUID, automation_id: uuid.UUID) -> Automation | None:
    return (
        db.query(Automation)
        .filter(Automation.id == automation_id, Automation.organization_id == organization_id)
        .first()
    )


def list_all(db: Session, organization_id: uuid.UUID) -> list[Automation]:
    return (
        db.query(Automation)
        .filter(Automation.organization_id == organization_id)
        .order_by(Automation.created_at.desc())
        .all()
    )


def delete(db: Session, automation: Automation) -> None:
    db.query(AutomationExecution).filter(
        AutomationExecution.automation_id == automation.id
    ).delete()
    db.delete(automation)
    db.flush()


def get_inactive_customers(db: Session, organization_id: uuid.UUID, cutoff: datetime) -> list[Customer]:
    """Clientes sin ninguna tarea creada después de 'cutoff'."""
    subquery = (
        select(Task.customer_id)
        .where(Task.customer_id.is_not(None), Task.created_at > cutoff)
        .distinct()
    )
    return (
        db.query(Customer)
        .filter(
            Customer.organization_id == organization_id,
            Customer.deleted_at.is_(None),
            not_(Customer.id.in_(subquery)),
        )
        .all()
    )


def log_execution(
    db: Session,
    automation_id: uuid.UUID,
    organization_id: uuid.UUID,
    status: str,
    trigger_context: dict,
    result: dict | None,
) -> AutomationExecution:
    execution = AutomationExecution(
        automation_id=automation_id,
        organization_id=organization_id,
        status=status,
        trigger_context=trigger_context,
        result=result,
        finished_at=datetime.now(timezone.utc),
    )
    db.add(execution)
    db.flush()
    return execution


def list_executions(db: Session, organization_id: uuid.UUID, automation_id: uuid.UUID) -> list[AutomationExecution]:
    return (
        db.query(AutomationExecution)
        .filter(
            AutomationExecution.organization_id == organization_id,
            AutomationExecution.automation_id == automation_id,
        )
        .order_by(AutomationExecution.started_at.desc())
        .all()
    )