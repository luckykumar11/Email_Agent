from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.agent import GenerateEmailRequest, GeneratedEmailResponse
from app.services import agent_service

router = APIRouter(prefix="/agent", tags=["Email Agent"])


@router.post("/generate-email", response_model=GeneratedEmailResponse)
async def generate_email(
    data: GenerateEmailRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await agent_service.generate_email(db, user, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
