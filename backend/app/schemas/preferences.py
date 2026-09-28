from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PreferencesCreate(BaseModel):
    sender_name: Optional[str] = None
    reply_to: Optional[str] = None
    default_signature: bool = True
    append_signature: bool = True
    email_format: str = "html"
    default_cc: Optional[str] = None
    default_bcc: Optional[str] = None
    sending_limit: Optional[int] = None


class PreferencesUpdate(BaseModel):
    sender_name: Optional[str] = None
    reply_to: Optional[str] = None
    default_signature: Optional[bool] = None
    append_signature: Optional[bool] = None
    email_format: Optional[str] = None
    default_cc: Optional[str] = None
    default_bcc: Optional[str] = None
    sending_limit: Optional[int] = None


class PreferencesResponse(BaseModel):
    id: int
    sender_name: Optional[str] = None
    reply_to: Optional[str] = None
    default_signature: bool
    append_signature: bool
    email_format: str
    default_cc: Optional[str] = None
    default_bcc: Optional[str] = None
    sending_limit: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
