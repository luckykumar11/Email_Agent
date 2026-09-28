from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.email_history import EmailHistory


async def create_email_history(db: AsyncSession, record: EmailHistory) -> EmailHistory:
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_email_history(
    db: AsyncSession, company_id: int, page: int = 1, page_size: int = 20
) -> tuple[list[EmailHistory], int]:
    count_result = await db.execute(
        select(func.count(EmailHistory.id)).where(EmailHistory.company_id == company_id)
    )
    total = count_result.scalar()

    result = await db.execute(
        select(EmailHistory)
        .where(EmailHistory.company_id == company_id)
        .order_by(EmailHistory.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    emails = list(result.scalars().all())
    return emails, total
