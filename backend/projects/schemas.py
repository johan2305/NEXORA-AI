import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    customer_id: uuid.UUID | None = None
    status: str = "planning"
    start_date: date | None = None
    end_date: date | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    customer_id: uuid.UUID | None = None
    status: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    customer_id: uuid.UUID | None
    status: str
    start_date: date | None
    end_date: date | None
    created_at: datetime
    updated_at: datetime