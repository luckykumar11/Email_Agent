from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.company_repository import get_company_by_user_id
from app.schemas.email_config import (
    EmailConfigCreate,
    EmailConfigUpdate,
    EmailConfigResponse,
    SMTPTestRequest,
    SMTPTestResponse,
)
from app.services import email_config_service
from app.services.smtp_service import verify_smtp_connection

router = APIRouter(prefix="/email-config", tags=["Email Configuration"])


@router.post("", response_model=EmailConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_config(
    data: EmailConfigCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return await email_config_service.create_config(db, company.id, data)


@router.get("", response_model=EmailConfigResponse | None)
async def get_config(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        return None
    result = await email_config_service.get_config(db, company.id)
    return result


@router.put("", response_model=EmailConfigResponse)
async def update_config(
    data: EmailConfigUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return await email_config_service.update_config(db, company.id, data)


@router.post("/test", response_model=SMTPTestResponse)
async def test_config(
    data: SMTPTestRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    config = await email_config_service.get_raw_config(db, company.id)
    success, message = verify_smtp_connection(config, data.recipient)
    return SMTPTestResponse(success=success, message=message)
