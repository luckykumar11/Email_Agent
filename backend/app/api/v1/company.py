from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.services import company_service

router = APIRouter(prefix="/company", tags=["Company"])


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    data: CompanyCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await company_service.create_company_profile(db, user.id, data)


@router.get("", response_model=CompanyResponse | None)
async def get_company(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await company_service.get_company(db, user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return result


@router.put("", response_model=CompanyResponse)
async def update_company(
    data: CompanyUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await company_service.update_company_profile(db, user.id, data)
