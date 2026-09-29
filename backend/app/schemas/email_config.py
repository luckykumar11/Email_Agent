from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class EmailConfigCreate(BaseModel):
    email_address: EmailStr
    smtp_host: str
    smtp_port: int
    username: str
    password: str
    security_type: str = "NONE"
    sender_name: Optional[str] = None
    reply_to: Optional[EmailStr] = None

    @field_validator("reply_to", "sender_name", mode="before")
    @classmethod
    def empty_to_none(cls, v):
        return None if v == "" else v

    @field_validator("security_type")
    @classmethod
    def validate_security_type(cls, v: str) -> str:
        valid = {"NONE", "STARTTLS", "SSL_TLS"}
        if v.upper() not in valid:
            raise ValueError(f"security_type must be one of: {', '.join(valid)}")
        return v.upper()

    @field_validator("smtp_port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not (1 <= v <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        return v


class EmailConfigUpdate(BaseModel):
    email_address: Optional[EmailStr] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    security_type: Optional[str] = None
    sender_name: Optional[str] = None
    reply_to: Optional[EmailStr] = None

    @field_validator("reply_to", "sender_name", mode="before")
    @classmethod
    def empty_to_none(cls, v):
        return None if v == "" else v

    @field_validator("security_type")
    @classmethod
    def validate_security_type(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        valid = {"NONE", "STARTTLS", "SSL_TLS"}
        if v.upper() not in valid:
            raise ValueError(f"security_type must be one of: {', '.join(valid)}")
        return v.upper()


class EmailConfigResponse(BaseModel):
    id: int
    email_address: str
    smtp_host: str
    smtp_port: int
    username: str
    password_configured: bool = True
    security_type: str
    sender_name: Optional[str] = None
    reply_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SMTPTestRequest(BaseModel):
    recipient: EmailStr


class SMTPTestResponse(BaseModel):
    success: bool
    message: str
