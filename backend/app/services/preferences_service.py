from sqlalchemy.ext.asyncio import AsyncSession

from app.models.preferences import EmailPreference
from app.repositories.preferences_repository import (
    get_preferences_by_company_id,
    create_preferences,
    update_preferences,
)
from app.schemas.preferences import PreferencesCreate, PreferencesUpdate, PreferencesResponse


async def get_prefs(db: AsyncSession, company_id: int) -> PreferencesResponse | None:
    prefs = await get_preferences_by_company_id(db, company_id)
    if not prefs:
        return None
    return PreferencesResponse.model_validate(prefs)


async def upsert_prefs(db: AsyncSession, company_id: int, data: PreferencesCreate) -> PreferencesResponse:
    prefs = await get_preferences_by_company_id(db, company_id)
    if prefs:
        for key, value in data.model_dump().items():
            setattr(prefs, key, value)
        prefs = await update_preferences(db, prefs)
    else:
        prefs = EmailPreference(company_id=company_id, **data.model_dump())
        prefs = await create_preferences(db, prefs)
    return PreferencesResponse.model_validate(prefs)


async def update_prefs(db: AsyncSession, company_id: int, data: PreferencesUpdate) -> PreferencesResponse:
    prefs = await get_preferences_by_company_id(db, company_id)
    if not prefs:
        prefs = EmailPreference(company_id=company_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(prefs, key, value)
        prefs = await create_preferences(db, prefs)
    else:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(prefs, key, value)
        prefs = await update_preferences(db, prefs)
    return PreferencesResponse.model_validate(prefs)


async def get_raw_prefs(db: AsyncSession, company_id: int) -> EmailPreference | None:
    return await get_preferences_by_company_id(db, company_id)
