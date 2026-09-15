import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.projects.models import Project


def create(db: Session, organization_id: uuid.UUID, data: dict) -> Project:
    project = Project(organization_id=organization_id, **data)
    db.add(project)
    db.flush()
    return project


def get_by_id(db: Session, organization_id: uuid.UUID, project_id: uuid.UUID) -> Project | None:
    return (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == organization_id,
            Project.deleted_at.is_(None),
        )
        .first()
    )


def list_all(db: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 50) -> list[Project]:
    return (
        db.query(Project)
        .filter(Project.organization_id == organization_id, Project.deleted_at.is_(None))
        .order_by(Project.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update(db: Session, project: Project, data: dict) -> Project:
    for key, value in data.items():
        if value is not None:
            setattr(project, key, value)
    db.flush()
    return project


def soft_delete(db: Session, project: Project) -> None:
    project.deleted_at = datetime.now(timezone.utc)
    db.flush()