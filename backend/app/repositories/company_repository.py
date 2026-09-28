from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.company import Company


async def get_company_by_user_id(db: AsyncSession, user_id: int) -> Company | None:
    result = await db.execute(
        select(Company)
        .options(
            selectinload(Company.services_products),
            selectinload(Company.target_customers),
            selectinload(Company.value_propositions),
            selectinload(Company.social_links),
        )
        .where(Company.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_company_by_id(db: AsyncSession, company_id: int) -> Company | None:
    result = await db.execute(
        select(Company)
        .options(
            selectinload(Company.services_products),
            selectinload(Company.target_customers),
            selectinload(Company.value_propositions),
            selectinload(Company.social_links),
        )
        .where(Company.id == company_id)
    )
    return result.scalar_one_or_none()


async def create_company(db: AsyncSession, company: Company) -> Company:
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


async def update_company(db: AsyncSession, company: Company) -> Company:
    await db.commit()
    await db.refresh(company)
    return company
