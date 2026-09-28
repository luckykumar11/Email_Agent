import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login, auth_headers


async def setup_full_company(client: AsyncClient, email: str) -> str:
    token = await register_and_login(client, email)
    await client.post("/api/v1/company", headers=auth_headers(token), json={
        "name": "AI Corp",
        "description": "AI solutions company",
        "industry": "Technology",
        "services_products": [{"name": "AI Platform", "description": "ML platform"}],
        "target_customers": [{"description": "Enterprises"}],
        "value_propositions": [{"description": "Automate workflows"}],
    })
    return token


@pytest.mark.asyncio
async def test_generate_email(client: AsyncClient):
    token = await setup_full_company(client, "agent1@example.com")
    resp = await client.post("/api/v1/agent/generate-email", headers=auth_headers(token), json={
        "recipient_name": "Rahul",
        "recipient_email": "rahul@example.com",
        "purpose": "Introduce our AI platform",
        "tone": "professional",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "subject" in data
    assert "body" in data
    assert data["recipient_name"] == "Rahul"
    assert data["recipient_email"] == "rahul@example.com"


@pytest.mark.asyncio
async def test_generate_email_no_company(client: AsyncClient):
    token = await register_and_login(client, "agent2@example.com")
    resp = await client.post("/api/v1/agent/generate-email", headers=auth_headers(token), json={
        "recipient_name": "Rahul",
        "recipient_email": "rahul@example.com",
        "purpose": "Test",
        "tone": "formal",
    })
    assert resp.status_code == 400
