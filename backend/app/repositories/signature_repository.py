from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.signature import EmailSignature


async def get_signature_by_company_id(db: AsyncSession, company_id: int) -> EmailSignature | None:
    result = await db.execute(
        select(EmailSignature).where(EmailSignature.company_id == company_id)
    )
    return result.scalar_one_or_none()


async def create_signature(db: AsyncSession, sig: EmailSignature) -> EmailSignature:
    db.add(sig)
    await db.commit()
    await db.refresh(sig)
    return sig


async def update_signature(db: AsyncSession, sig: EmailSignature) -> EmailSignature:
    await db.commit()
    await db.refresh(sig)
    return sig


async def delete_signature(db: AsyncSession, sig: EmailSignature) -> None:
    await db.delete(sig)
    await db.commit()
