from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.company_repository import get_company_by_user_id
from app.schemas.signature import SignatureCreate, SignatureUpdate, SignatureResponse
from app.services import signature_service

router = APIRouter(prefix="/signature", tags=["Email Signature"])


@router.post("", response_model=SignatureResponse, status_code=status.HTTP_201_CREATED)
async def create_signature(
    data: SignatureCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return await signature_service.create_sig(db, company.id, data)


@router.get("", response_model=SignatureResponse | None)
async def get_signature(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    result = await signature_service.get_sig(db, company.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signature not found")
    return result


@router.put("", response_model=SignatureResponse)
async def update_signature(
    data: SignatureUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return await signature_service.update_sig(db, company.id, data)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_signature_endpoint(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    await signature_service.delete_sig(db, company.id)
