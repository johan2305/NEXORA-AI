import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SmartTaskRequest(BaseModel):
    text: str


class SmartTaskExtraction(BaseModel):
    title: str
    priority: str
    due_date_hint: str | None = None
    reasoning: str


class AIRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    module: str
    provider: str
    latency_ms: int | None
    created_at: datetime