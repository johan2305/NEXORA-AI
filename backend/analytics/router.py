from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.analytics import service as analytics_service
from backend.analytics.schemas import AnalyticsSummary
from backend.core.database import get_db
from backend.core.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def get_summary(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return analytics_service.get_summary(db, current_user.organization_id)