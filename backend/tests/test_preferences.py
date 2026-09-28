import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login, auth_headers


async def setup_company(client: AsyncClient, email: str) -> str:
    token = await register_and_login(client, email)
    await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "Pref Co"})
    return token


@pytest.mark.asyncio
async def test_create_preferences(client: AsyncClient):
    token = await setup_company(client, "pref1@example.com")
    resp = await client.post("/api/v1/preferences", headers=auth_headers(token), json={
        "sender_name": "Test Sender",
        "reply_to": "reply@example.com",
        "email_format": "html",
        "default_signature": True,
        "append_signature": True,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["sender_name"] == "Test Sender"
    assert data["email_format"] == "html"


@pytest.mark.asyncio
async def test_get_preferences(client: AsyncClient):
    token = await setup_company(client, "pref2@example.com")
    await client.post("/api/v1/preferences", headers=auth_headers(token), json={
        "sender_name": "Get Me",
        "email_format": "plain",
    })
    resp = await client.get("/api/v1/preferences", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["sender_name"] == "Get Me"
    assert resp.json()["email_format"] == "plain"


@pytest.mark.asyncio
async def test_update_preferences(client: AsyncClient):
    token = await setup_company(client, "pref3@example.com")
    await client.post("/api/v1/preferences", headers=auth_headers(token), json={
        "sender_name": "Old",
        "email_format": "html",
    })
    resp = await client.put("/api/v1/preferences", headers=auth_headers(token), json={
        "sender_name": "New",
        "email_format": "plain",
    })
    assert resp.status_code == 200
    assert resp.json()["sender_name"] == "New"
    assert resp.json()["email_format"] == "plain"
