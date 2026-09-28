from pydantic import BaseModel, EmailStr


class GenerateEmailRequest(BaseModel):
    recipient_name: str
    recipient_email: EmailStr
    purpose: str
    tone: str = "professional"
    additional_instructions: str = ""


class GeneratedEmailResponse(BaseModel):
    subject: str
    body: str
    recipient_name: str
    recipient_email: str
