import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login, auth_headers


async def setup_company(client: AsyncClient, email: str) -> str:
    token = await register_and_login(client, email)
    await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "Sig Co"})
    return token


@pytest.mark.asyncio
async def test_create_signature(client: AsyncClient):
    token = await setup_company(client, "sig1@example.com")
    resp = await client.post("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "Best Regards,\nJohn\nCEO",
        "enabled": True,
        "append_automatically": True,
    })
    assert resp.status_code == 201
    assert resp.json()["enabled"] is True


@pytest.mark.asyncio
async def test_get_signature(client: AsyncClient):
    token = await setup_company(client, "sig2@example.com")
    await client.post("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "John Doe",
        "enabled": True,
        "append_automatically": False,
    })
    resp = await client.get("/api/v1/signature", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["signature_text"] == "John Doe"


@pytest.mark.asyncio
async def test_update_signature(client: AsyncClient):
    token = await setup_company(client, "sig3@example.com")
    await client.post("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "Old",
        "enabled": True,
        "append_automatically": True,
    })
    resp = await client.put("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "New signature",
        "enabled": False,
    })
    assert resp.status_code == 200
    assert resp.json()["signature_text"] == "New signature"
    assert resp.json()["enabled"] is False


@pytest.mark.asyncio
async def test_delete_signature(client: AsyncClient):
    token = await setup_company(client, "sig4@example.com")
    await client.post("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "Delete me",
        "enabled": True,
        "append_automatically": True,
    })
    resp = await client.delete("/api/v1/signature", headers=auth_headers(token))
    assert resp.status_code == 204
    resp = await client.get("/api/v1/signature", headers=auth_headers(token))
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_signature_not_found(client: AsyncClient):
    token = await setup_company(client, "sig5@example.com")
    resp = await client.get("/api/v1/signature", headers=auth_headers(token))
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_signature(client: AsyncClient):
    token = await setup_company(client, "sig6@example.com")
    await client.post("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "First",
        "enabled": True,
        "append_automatically": True,
    })
    resp = await client.post("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "Second",
        "enabled": True,
        "append_automatically": True,
    })
    assert resp.status_code == 409
