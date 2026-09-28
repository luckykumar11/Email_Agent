from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class ServiceProductCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ServiceProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class TargetCustomerCreate(BaseModel):
    description: str


class TargetCustomerResponse(BaseModel):
    id: int
    description: str

    model_config = {"from_attributes": True}


class ValuePropositionCreate(BaseModel):
    description: str


class ValuePropositionResponse(BaseModel):
    id: int
    description: str

    model_config = {"from_attributes": True}


class SocialLinkCreate(BaseModel):
    platform: str
    url: str


class SocialLinkResponse(BaseModel):
    id: int
    platform: str
    url: str

    model_config = {"from_attributes": True}


class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    services_products: List[ServiceProductCreate] = []
    target_customers: List[TargetCustomerCreate] = []
    value_propositions: List[ValuePropositionCreate] = []
    social_links: List[SocialLinkCreate] = []


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    services_products: Optional[List[ServiceProductCreate]] = None
    target_customers: Optional[List[TargetCustomerCreate]] = None
    value_propositions: Optional[List[ValuePropositionCreate]] = None
    social_links: Optional[List[SocialLinkCreate]] = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    services_products: List[ServiceProductResponse] = []
    target_customers: List[TargetCustomerResponse] = []
    value_propositions: List[ValuePropositionResponse] = []
    social_links: List[SocialLinkResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
