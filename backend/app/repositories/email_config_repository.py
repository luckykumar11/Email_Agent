from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.email_config import EmailConfiguration


async def get_email_config_by_company_id(db: AsyncSession, company_id: int) -> EmailConfiguration | None:
    result = await db.execute(
        select(EmailConfiguration).where(EmailConfiguration.company_id == company_id)
    )
    return result.scalar_one_or_none()


async def create_email_config(db: AsyncSession, config: EmailConfiguration) -> EmailConfiguration:
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


async def update_email_config(db: AsyncSession, config: EmailConfiguration) -> EmailConfiguration:
    await db.commit()
    await db.refresh(config)
    return config
