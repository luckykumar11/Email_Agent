from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.company_repository import get_company_by_user_id
from app.schemas.preferences import PreferencesCreate, PreferencesUpdate, PreferencesResponse
from app.services import preferences_service

router = APIRouter(prefix="/preferences", tags=["Email Preferences"])


@router.post("", response_model=PreferencesResponse, status_code=status.HTTP_201_CREATED)
async def create_preferences(
    data: PreferencesCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return await preferences_service.upsert_prefs(db, company.id, data)


@router.get("", response_model=PreferencesResponse | None)
async def get_preferences(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        return None
    result = await preferences_service.get_prefs(db, company.id)
    return result


@router.put("", response_model=PreferencesResponse)
async def update_preferences(
    data: PreferencesUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return await preferences_service.update_prefs(db, company.id, data)
