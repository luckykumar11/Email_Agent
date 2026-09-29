from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.email_config import EmailConfiguration
from app.repositories.email_config_repository import (
    get_email_config_by_company_id,
    create_email_config,
    update_email_config,
)
from app.schemas.email_config import EmailConfigCreate, EmailConfigUpdate, EmailConfigResponse


def _encrypt_password(password: str) -> str:
    from app.core.security import encrypt_password
    return encrypt_password(password)


def _decrypt_password(encrypted: str) -> str:
    from app.core.security import decrypt_password
    return decrypt_password(encrypted)


def _to_response(config: EmailConfiguration) -> EmailConfigResponse:
    return EmailConfigResponse(
        id=config.id,
        email_address=config.email_address,
        smtp_host=config.smtp_host,
        smtp_port=config.smtp_port,
        username=config.username,
        password_configured=True,
        security_type=config.security_type,
        sender_name=config.sender_name,
        reply_to=config.reply_to,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


async def get_config(db: AsyncSession, company_id: int) -> EmailConfigResponse | None:
    config = await get_email_config_by_company_id(db, company_id)
    if not config:
        return None
    return _to_response(config)


async def create_config(db: AsyncSession, company_id: int, data: EmailConfigCreate) -> EmailConfigResponse:
    existing = await get_email_config_by_company_id(db, company_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email configuration already exists for this company",
        )
    config = EmailConfiguration(
        company_id=company_id,
        email_address=data.email_address,
        smtp_host=data.smtp_host,
        smtp_port=data.smtp_port,
        username=data.username,
        encrypted_password=_encrypt_password(data.password),
        security_type=data.security_type,
        sender_name=data.sender_name,
        reply_to=data.reply_to,
    )
    config = await create_email_config(db, config)
    return _to_response(config)


async def update_config(db: AsyncSession, company_id: int, data: EmailConfigUpdate) -> EmailConfigResponse:
    config = await get_email_config_by_company_id(db, company_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        config.encrypted_password = _encrypt_password(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(config, key, value)
    config = await update_email_config(db, config)
    return _to_response(config)


async def get_raw_config(db: AsyncSession, company_id: int) -> EmailConfiguration:
    config = await get_email_config_by_company_id(db, company_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found",
        )
    return config
