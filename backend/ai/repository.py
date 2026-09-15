import uuid

from sqlalchemy.orm import Session

from backend.ai.models import AIRequest


def log_request(
    db: Session,
    organization_id: uuid.UUID,
    user_id: uuid.UUID | None,
    module: str,
    prompt: str,
    response: dict,
    latency_ms: int,
) -> AIRequest:
    ai_request = AIRequest(
        organization_id=organization_id,
        user_id=user_id,
        module=module,
        prompt=prompt,
        response=response,
        latency_ms=latency_ms,
    )
    db.add(ai_request)
    db.flush()
    return ai_request