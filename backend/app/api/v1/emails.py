from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.email import SendEmailRequest, SendEmailResponse, EmailHistoryListResponse
from app.services import email_service

router = APIRouter(prefix="/emails", tags=["Emails"])


@router.post("/send", response_model=SendEmailResponse)
async def send_email(
    data: SendEmailRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await email_service.send_email(db, user, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/history", response_model=EmailHistoryListResponse)
async def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await email_service.get_history(db, user, page, page_size)
