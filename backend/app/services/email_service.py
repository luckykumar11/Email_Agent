from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.email_history import EmailHistory
from app.repositories.company_repository import get_company_by_user_id
from app.repositories.email_history_repository import create_email_history
from app.schemas.email import SendEmailRequest, SendEmailResponse, EmailHistoryResponse, EmailHistoryListResponse
from app.services.email_config_service import get_raw_config
from app.services.signature_service import get_raw_signature
from app.services.preferences_service import get_raw_prefs
from app.services.smtp_service import send_smtp_email
from app.repositories.email_history_repository import get_email_history


async def send_email(
    db: AsyncSession, user: User, request: SendEmailRequest
) -> SendEmailResponse:
    company = await get_company_by_user_id(db, user.id)
    if not company:
        raise ValueError("Company profile not found")

    config = await get_raw_config(db, company.id)

    prefs = await get_raw_prefs(db, company.id)
    sig = await get_raw_signature(db, company.id)

    sender_name = None
    reply_to = None
    email_format = request.format

    if prefs:
        sender_name = prefs.sender_name or config.sender_name
        reply_to = prefs.reply_to or config.reply_to
        if prefs.default_signature and prefs.append_signature and sig and sig.enabled:
            request.body = request.body + "\n\n" + sig.signature_text
    else:
        sender_name = config.sender_name
        reply_to = config.reply_to

    success, message = send_smtp_email(
        config=config,
        sender_name=sender_name or config.sender_name,
        reply_to=reply_to or config.reply_to,
        recipient=request.recipient,
        subject=request.subject,
        body=request.body,
        format=email_format,
        cc=[str(c) for c in request.cc] if request.cc else None,
        bcc=[str(b) for b in request.bcc] if request.bcc else None,
        password_override=None,
    )

    history = EmailHistory(
        company_id=company.id,
        sender=config.email_address,
        recipient=request.recipient,
        cc=", ".join([str(c) for c in request.cc]) if request.cc else None,
        bcc=", ".join([str(b) for b in request.bcc]) if request.bcc else None,
        subject=request.subject,
        status="sent" if success else "failed",
        format=email_format,
        failure_reason=None if success else message,
    )
    await create_email_history(db, history)

    return SendEmailResponse(
        success=success,
        message=message,
        email_id=history.id,
    )


async def get_history(
    db: AsyncSession, user: User, page: int = 1, page_size: int = 20
) -> EmailHistoryListResponse:
    company = await get_company_by_user_id(db, user.id)
    if not company:
        return EmailHistoryListResponse(emails=[], total=0, page=page, page_size=page_size)

    emails, total = await get_email_history(db, company.id, page, page_size)
    return EmailHistoryListResponse(
        emails=[EmailHistoryResponse.model_validate(e) for e in emails],
        total=total,
        page=page,
        page_size=page_size,
    )
