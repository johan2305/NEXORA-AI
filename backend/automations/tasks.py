from backend.automations import service as automation_service
from backend.automations.models import Automation
from backend.core.celery_app import celery_app
from backend.core.database import SessionLocal


@celery_app.task(name="backend.automations.tasks.run_all_automations_task")
def run_all_automations_task():
    """
    Se ejecuta periódicamente (ver beat_schedule en celery_app.py).
    Revisa TODAS las automatizaciones activas de TODAS las organizaciones
    y las ejecuta una por una.
    """
    db = SessionLocal()
    results = []
    try:
        automations = db.query(Automation).filter(Automation.is_active.is_(True)).all()

        for automation in automations:
            try:
                result = automation_service.run_automation(
                    db, automation.organization_id, automation.id
                )
                results.append({"automation_id": str(automation.id), "result": result})
            except Exception as exc:
                results.append({"automation_id": str(automation.id), "error": str(exc)})

        return results
    finally:
        db.close()