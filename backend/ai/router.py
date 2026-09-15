from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.ai import service as ai_service
from backend.core.database import get_db
from backend.core.dependencies import get_current_user, CurrentUser
from backend.tasks import service as task_service
from backend.tasks.schemas import TaskCreate, TaskResponse
from backend.ai.schemas import SmartTaskRequest

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/smart-task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_smart_task(
    data: SmartTaskRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        extraction = ai_service.extract_task_from_text(
            db, current_user.organization_id, current_user.user.id, data.text
        )
    except ai_service.AIServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

    task_data = TaskCreate(title=extraction.title, priority=extraction.priority)
    return task_service.create_task(db, current_user.organization_id, task_data, created_by="ai")