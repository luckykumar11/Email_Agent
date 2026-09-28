from datetime import datetime
from pydantic import BaseModel


class SignatureCreate(BaseModel):
    signature_text: str
    enabled: bool = True
    append_automatically: bool = True


class SignatureUpdate(BaseModel):
    signature_text: str | None = None
    enabled: bool | None = None
    append_automatically: bool | None = None


class SignatureResponse(BaseModel):
    id: int
    signature_text: str
    enabled: bool
    append_automatically: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
