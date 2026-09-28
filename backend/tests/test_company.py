import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login, auth_headers


@pytest.mark.asyncio
async def test_create_company(client: AsyncClient):
    token = await register_and_login(client, "company@example.com")
    resp = await client.post("/api/v1/company", headers=auth_headers(token), json={
        "name": "Test Corp",
        "description": "A test company",
        "industry": "Technology",
        "services_products": [{"name": "CRM", "description": "Sales tool"}],
        "target_customers": [{"description": "Small businesses"}],
        "value_propositions": [{"description": "Increase sales"}],
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Corp"
    assert len(data["services_products"]) == 1
    assert data["services_products"][0]["name"] == "CRM"


@pytest.mark.asyncio
async def test_get_company(client: AsyncClient):
    token = await register_and_login(client, "getcompany@example.com")
    await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "My Co"})
    resp = await client.get("/api/v1/company", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["name"] == "My Co"


@pytest.mark.asyncio
async def test_update_company(client: AsyncClient):
    token = await register_and_login(client, "updatecompany@example.com")
    await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "Old Name"})
    resp = await client.put("/api/v1/company", headers=auth_headers(token), json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


@pytest.mark.asyncio
async def test_company_not_found(client: AsyncClient):
    token = await register_and_login(client, "nocompany@example.com")
    resp = await client.get("/api/v1/company", headers=auth_headers(token))
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_company_isolation(client: AsyncClient):
    token_a = await register_and_login(client, "usera@example.com")
    token_b = await register_and_login(client, "userb@example.com")

    await client.post("/api/v1/company", headers=auth_headers(token_a), json={"name": "Company A"})
    await client.post("/api/v1/company", headers=auth_headers(token_b), json={"name": "Company B"})

    resp_a = await client.get("/api/v1/company", headers=auth_headers(token_a))
    resp_b = await client.get("/api/v1/company", headers=auth_headers(token_b))

    assert resp_a.json()["name"] == "Company A"
    assert resp_b.json()["name"] == "Company B"


@pytest.mark.asyncio
async def test_duplicate_company(client: AsyncClient):
    token = await register_and_login(client, "dupcompany@example.com")
    await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "First"})
    resp = await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "Second"})
    assert resp.status_code == 409
