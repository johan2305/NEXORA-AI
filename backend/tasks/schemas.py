import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    project_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    assignee_id: uuid.UUID | None = None
    status: str = "todo"
    priority: str = "medium"
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    project_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    assignee_id: uuid.UUID | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    project_id: uuid.UUID | None
    customer_id: uuid.UUID | None
    assignee_id: uuid.UUID | None
    status: str
    priority: str
    due_date: datetime | None
    created_by: str
    created_at: datetime
    updated_at: datetime