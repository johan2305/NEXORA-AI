import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from backend.automations import repository as automation_repository
from backend.automations.schemas import AutomationCreate
from backend.tasks import service as task_service
from backend.tasks.schemas import TaskCreate
from backend.notifications import repository as notification_repository
from backend.notifications import publisher as notification_publisher
from backend.audit import repository as audit_repository


class AutomationNotFoundError(Exception):
    pass


class UnsupportedTriggerError(Exception):
    pass


def create_automation(db: Session, organization_id: uuid.UUID, data: AutomationCreate):
    automation = automation_repository.create(db, organization_id, data.model_dump())
    db.commit()
    db.refresh(automation)
    return automation


def get_automation(db: Session, organization_id: uuid.UUID, automation_id: uuid.UUID):
    automation = automation_repository.get_by_id(db, organization_id, automation_id)
    if not automation:
        raise AutomationNotFoundError("Automation not found")
    return automation


def list_automations(db: Session, organization_id: uuid.UUID):
    return automation_repository.list_all(db, organization_id)


def delete_automation(db: Session, organization_id: uuid.UUID, automation_id: uuid.UUID):
    automation = get_automation(db, organization_id, automation_id)
    automation_repository.delete(db, automation)
    db.commit()


def list_executions(db: Session, organization_id: uuid.UUID, automation_id: uuid.UUID):
    get_automation(db, organization_id, automation_id)  # valida que exista y sea de esta org
    return automation_repository.list_executions(db, organization_id, automation_id)


def run_automation(db: Session, organization_id: uuid.UUID, automation_id: uuid.UUID):
    """
    Evalúa el trigger de una automatización y ejecuta su acción si aplica.
    Por ahora se dispara manualmente (POST /run); en el Día 9 lo conectamos
    a Celery para que corra solo en segundo plano.
    """
    automation = get_automation(db, organization_id, automation_id)

    if not automation.is_active:
        return {"executed": 0, "reason": "automation is inactive"}

    if automation.trigger_type == "customer_inactive":
        return _run_customer_inactive(db, automation)

    raise UnsupportedTriggerError(f"Trigger type '{automation.trigger_type}' not supported yet")


def _run_customer_inactive(db: Session, automation):
    days = automation.trigger_config.get("days_inactive", 7)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    inactive_customers = automation_repository.get_inactive_customers(
        db, automation.organization_id, cutoff
    )

    executed = 0
    for customer in inactive_customers:
        if automation.action_type == "create_task":
            title_template = automation.action_config.get(
                "title_template", "Seguimiento con {customer_name}"
            )
            title = title_template.replace("{customer_name}", customer.name)

            task_service.create_task(
                db,
                automation.organization_id,
                TaskCreate(title=title, customer_id=customer.id, priority="medium"),
                created_by="automation",
            )

            notification_repository.create(
                db,
                organization_id=automation.organization_id,
                type="automation_triggered",
                title="Automatización ejecutada",
                message=f"Se creó una tarea de seguimiento: {title}",
            )

            notification_publisher.publish_notification(
                str(automation.organization_id),
                {
                    "type": "automation_triggered",
                    "title": "Automatización ejecutada",
                    "message": f"Se creó una tarea de seguimiento: {title}",
                },
            )

            automation_repository.log_execution(
                db,
                automation_id=automation.id,
                organization_id=automation.organization_id,
                status="success",
                trigger_context={"customer_id": str(customer.id), "customer_name": customer.name},
                result={"action": "create_task", "title": title},
            )

            audit_repository.log(
                db,
                organization_id=automation.organization_id,
                action="AUTOMATION_EXECUTED",
                resource_type="automation",
                resource_id=automation.id,
                metadata={"customer_id": str(customer.id), "task_title": title},
            )

            executed += 1

    db.commit()
    return {"executed": executed, "customers_evaluated": len(inactive_customers)}