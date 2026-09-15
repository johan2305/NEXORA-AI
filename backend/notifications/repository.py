import uuid

from sqlalchemy.orm import Session

from backend.notifications.models import Notification


def create(db: Session, organization_id: uuid.UUID, type: str, title: str, message: str, metadata: dict | None = None) -> Notification:
    notification = Notification(
        organization_id=organization_id,
        type=type,
        title=title,
        message=message,
        notification_metadata=metadata,
    )
    db.add(notification)
    db.flush()
    return notification


def list_all(db: Session, organization_id: uuid.UUID, limit: int = 30) -> list[Notification]:
    return (
        db.query(Notification)
        .filter(Notification.organization_id == organization_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .all()
    )


def mark_as_read(db: Session, organization_id: uuid.UUID, notification_id: uuid.UUID) -> None:
    db.query(Notification).filter(
        Notification.id == notification_id, Notification.organization_id == organization_id
    ).update({"is_read": True})
    db.flush()