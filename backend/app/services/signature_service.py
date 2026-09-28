from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.signature import EmailSignature
from app.repositories.signature_repository import (
    get_signature_by_company_id,
    create_signature,
    update_signature,
    delete_signature,
)
from app.schemas.signature import SignatureCreate, SignatureUpdate, SignatureResponse


async def get_sig(db: AsyncSession, company_id: int) -> SignatureResponse | None:
    sig = await get_signature_by_company_id(db, company_id)
    if not sig:
        return None
    return SignatureResponse.model_validate(sig)


async def create_sig(db: AsyncSession, company_id: int, data: SignatureCreate) -> SignatureResponse:
    existing = await get_signature_by_company_id(db, company_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Signature already exists for this company",
        )
    sig = EmailSignature(
        company_id=company_id,
        signature_text=data.signature_text,
        enabled=data.enabled,
        append_automatically=data.append_automatically,
    )
    sig = await create_signature(db, sig)
    return SignatureResponse.model_validate(sig)


async def update_sig(db: AsyncSession, company_id: int, data: SignatureUpdate) -> SignatureResponse:
    sig = await get_signature_by_company_id(db, company_id)
    if not sig:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signature not found",
        )
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sig, key, value)
    sig = await update_signature(db, sig)
    return SignatureResponse.model_validate(sig)


async def delete_sig(db: AsyncSession, company_id: int) -> None:
    sig = await get_signature_by_company_id(db, company_id)
    if not sig:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signature not found",
        )
    await delete_signature(db, sig)


async def get_raw_signature(db: AsyncSession, company_id: int) -> EmailSignature | None:
    return await get_signature_by_company_id(db, company_id)
