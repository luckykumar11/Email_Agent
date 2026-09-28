from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company, ServiceProduct, TargetCustomer, ValueProposition, SocialLink
from app.repositories.company_repository import get_company_by_user_id, get_company_by_id, create_company, update_company
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse


async def get_company(db: AsyncSession, user_id: int) -> CompanyResponse | None:
    company = await get_company_by_user_id(db, user_id)
    if not company:
        return None
    return CompanyResponse.model_validate(company)


async def create_company_profile(db: AsyncSession, user_id: int, data: CompanyCreate) -> CompanyResponse:
    existing = await get_company_by_user_id(db, user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company profile already exists for this user",
        )
    company = Company(user_id=user_id, name=data.name)
    for attr in ["description", "website", "industry", "location", "contact_person", "contact_email", "contact_phone", "address"]:
        val = getattr(data, attr)
        if val is not None:
            setattr(company, attr, val)

    for sp in data.services_products:
        company.services_products.append(ServiceProduct(name=sp.name, description=sp.description))
    for tc in data.target_customers:
        company.target_customers.append(TargetCustomer(description=tc.description))
    for vp in data.value_propositions:
        company.value_propositions.append(ValueProposition(description=vp.description))
    for sl in data.social_links:
        company.social_links.append(SocialLink(platform=sl.platform, url=sl.url))

    company = await create_company(db, company)
    company = await get_company_by_id(db, company.id)
    return CompanyResponse.model_validate(company)


async def update_company_profile(db: AsyncSession, user_id: int, data: CompanyUpdate) -> CompanyResponse:
    company = await get_company_by_user_id(db, user_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    relational_fields = {"services_products", "target_customers", "value_propositions", "social_links"}
    for key, value in update_data.items():
        if key in relational_fields:
            continue
        setattr(company, key, value)

    if data.services_products is not None:
        company.services_products.clear()
        for sp in data.services_products:
            company.services_products.append(ServiceProduct(name=sp.name, description=sp.description))

    if data.target_customers is not None:
        company.target_customers.clear()
        for tc in data.target_customers:
            company.target_customers.append(TargetCustomer(description=tc.description))

    if data.value_propositions is not None:
        company.value_propositions.clear()
        for vp in data.value_propositions:
            company.value_propositions.append(ValueProposition(description=vp.description))

    if data.social_links is not None:
        company.social_links.clear()
        for sl in data.social_links:
            company.social_links.append(SocialLink(platform=sl.platform, url=sl.url))

    company = await update_company(db, company)
    company = await get_company_by_id(db, company.id)
    return CompanyResponse.model_validate(company)
