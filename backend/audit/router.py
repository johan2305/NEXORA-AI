from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.audit import repository as audit_repository
from backend.audit.schemas import ActivityLogResponse
from backend.core.database import get_db
from backend.core.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs", response_model=list[ActivityLogResponse])
def list_logs(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return audit_repository.list_all(db, current_user.organization_id)