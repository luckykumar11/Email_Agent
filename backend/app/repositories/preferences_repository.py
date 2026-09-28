from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.preferences import EmailPreference


async def get_preferences_by_company_id(db: AsyncSession, company_id: int) -> EmailPreference | None:
    result = await db.execute(
        select(EmailPreference).where(EmailPreference.company_id == company_id)
    )
    return result.scalar_one_or_none()


async def create_preferences(db: AsyncSession, prefs: EmailPreference) -> EmailPreference:
    db.add(prefs)
    await db.commit()
    await db.refresh(prefs)
    return prefs


async def update_preferences(db: AsyncSession, prefs: EmailPreference) -> EmailPreference:
    await db.commit()
    await db.refresh(prefs)
    return prefs
