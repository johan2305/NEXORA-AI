import uuid

from sqlalchemy.orm import Session

from backend.tasks import repository as task_repository
from backend.tasks.schemas import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    pass


def create_task(db: Session, organization_id: uuid.UUID, data: TaskCreate, created_by: str = "user"):
    task = task_repository.create(db, organization_id, data.model_dump(), created_by=created_by)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, organization_id: uuid.UUID, task_id: uuid.UUID):
    task = task_repository.get_by_id(db, organization_id, task_id)
    if not task:
        raise TaskNotFoundError("Task not found")
    return task


def list_tasks(db: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 50):
    return task_repository.list_all(db, organization_id, skip, limit)


def update_task(db: Session, organization_id: uuid.UUID, task_id: uuid.UUID, data: TaskUpdate):
    task = get_task(db, organization_id, task_id)
    task_repository.update(db, task, data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, organization_id: uuid.UUID, task_id: uuid.UUID):
    task = get_task(db, organization_id, task_id)
    task_repository.soft_delete(db, task)
    db.commit()