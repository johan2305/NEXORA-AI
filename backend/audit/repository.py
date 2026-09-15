import uuid

from sqlalchemy.orm import Session

from backend.audit.models import ActivityLog


def log(
    db: Session,
    organization_id: uuid.UUID,
    action: str,
    resource_type: str,
    user_id: uuid.UUID | None = None,
    resource_id: uuid.UUID | None = None,
    metadata: dict | None = None,
) -> ActivityLog:
    entry = ActivityLog(
        organization_id=organization_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        log_metadata=metadata,
    )
    db.add(entry)
    db.flush()
    return entry


def list_all(db: Session, organization_id: uuid.UUID, limit: int = 50) -> list[ActivityLog]:
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.organization_id == organization_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )