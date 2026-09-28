from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class SendEmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    format: str = "html"
    cc: List[EmailStr] = []
    bcc: List[EmailStr] = []


class SendEmailResponse(BaseModel):
    success: bool
    message: str
    email_id: Optional[int] = None


class EmailHistoryResponse(BaseModel):
    id: int
    sender: str
    recipient: str
    cc: Optional[str] = None
    bcc: Optional[str] = None
    subject: str
    status: str
    format: str
    failure_reason: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class EmailHistoryListResponse(BaseModel):
    emails: List[EmailHistoryResponse]
    total: int
    page: int
    page_size: int
