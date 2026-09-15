import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AutomationCreate(BaseModel):
    name: str
    description: str | None = None
    trigger_type: str
    trigger_config: dict = {}
    action_type: str
    action_config: dict = {}
    is_active: bool = True


class AutomationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    trigger_type: str
    trigger_config: dict
    action_type: str
    action_config: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AutomationExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    automation_id: uuid.UUID
    status: str
    trigger_context: dict
    result: dict | None
    started_at: datetime
    finished_at: datetime | None