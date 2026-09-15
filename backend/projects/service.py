import uuid

from sqlalchemy.orm import Session

from backend.projects import repository as project_repository
from backend.projects.schemas import ProjectCreate, ProjectUpdate


class ProjectNotFoundError(Exception):
    pass


def create_project(db: Session, organization_id: uuid.UUID, data: ProjectCreate):
    project = project_repository.create(db, organization_id, data.model_dump())
    db.commit()
    db.refresh(project)
    return project


def get_project(db: Session, organization_id: uuid.UUID, project_id: uuid.UUID):
    project = project_repository.get_by_id(db, organization_id, project_id)
    if not project:
        raise ProjectNotFoundError("Project not found")
    return project


def list_projects(db: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 50):
    return project_repository.list_all(db, organization_id, skip, limit)


def update_project(db: Session, organization_id: uuid.UUID, project_id: uuid.UUID, data: ProjectUpdate):
    project = get_project(db, organization_id, project_id)
    project_repository.update(db, project, data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, organization_id: uuid.UUID, project_id: uuid.UUID):
    project = get_project(db, organization_id, project_id)
    project_repository.soft_delete(db, project)
    db.commit()