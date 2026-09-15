import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.automations import service as automation_service
from backend.automations.schemas import (
    AutomationCreate,
    AutomationExecutionResponse,
    AutomationResponse,
)
from backend.core.database import get_db
from backend.core.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/automations", tags=["automations"])


@router.post("", response_model=AutomationResponse, status_code=status.HTTP_201_CREATED)
def create_automation(
    data: AutomationCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return automation_service.create_automation(db, current_user.organization_id, data)


@router.get("", response_model=list[AutomationResponse])
def list_automations(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return automation_service.list_automations(db, current_user.organization_id)


@router.delete("/{automation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_automation(
    automation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        automation_service.delete_automation(db, current_user.organization_id, automation_id)
    except automation_service.AutomationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")


@router.post("/{automation_id}/run")
def run_automation(
    automation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        return automation_service.run_automation(db, current_user.organization_id, automation_id)
    except automation_service.AutomationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")
    except automation_service.UnsupportedTriggerError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{automation_id}/executions", response_model=list[AutomationExecutionResponse])
def list_executions(
    automation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        return automation_service.list_executions(db, current_user.organization_id, automation_id)
    except automation_service.AutomationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found")