import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.tasks.models import Task


def create(db: Session, organization_id: uuid.UUID, data: dict, created_by: str = "user") -> Task:
    task = Task(organization_id=organization_id, created_by=created_by, **data)
    db.add(task)
    db.flush()
    return task


def get_by_id(db: Session, organization_id: uuid.UUID, task_id: uuid.UUID) -> Task | None:
    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.organization_id == organization_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )


def list_all(db: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 50) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.organization_id == organization_id, Task.deleted_at.is_(None))
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update(db: Session, task: Task, data: dict) -> Task:
    for key, value in data.items():
        if value is not None:
            setattr(task, key, value)
    db.flush()
    return task


def soft_delete(db: Session, task: Task) -> None:
    task.deleted_at = datetime.now(timezone.utc)
    db.flush()