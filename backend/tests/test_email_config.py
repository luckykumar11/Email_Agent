import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login, auth_headers


async def setup_company(client: AsyncClient, email: str) -> str:
    token = await register_and_login(client, email)
    await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "Test Co"})
    return token


@pytest.mark.asyncio
async def test_create_email_config(client: AsyncClient):
    token = await setup_company(client, "smtp1@example.com")
    resp = await client.post("/api/v1/email-config", headers=auth_headers(token), json={
        "email_address": "sender@example.com",
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "sender@example.com",
        "password": "apppassword",
        "security_type": "STARTTLS",
        "sender_name": "Test Sender",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email_address"] == "sender@example.com"
    assert data["password_configured"] is True
    assert "encrypted_password" not in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_email_config(client: AsyncClient):
    token = await setup_company(client, "smtp2@example.com")
    await client.post("/api/v1/email-config", headers=auth_headers(token), json={
        "email_address": "s@example.com",
        "smtp_host": "smtp.example.com",
        "smtp_port": 465,
        "username": "s@example.com",
        "password": "secret",
        "security_type": "SSL_TLS",
    })
    resp = await client.get("/api/v1/email-config", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["smtp_host"] == "smtp.example.com"


@pytest.mark.asyncio
async def test_password_not_returned(client: AsyncClient):
    token = await setup_company(client, "smtp3@example.com")
    await client.post("/api/v1/email-config", headers=auth_headers(token), json={
        "email_address": "s@example.com",
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "s@example.com",
        "password": "topsecret",
        "security_type": "STARTTLS",
    })
    resp = await client.get("/api/v1/email-config", headers=auth_headers(token))
    data = resp.json()
    assert "password" not in data
    assert "encrypted_password" not in data
    assert data["password_configured"] is True


@pytest.mark.asyncio
async def test_update_email_config(client: AsyncClient):
    token = await setup_company(client, "smtp4@example.com")
    await client.post("/api/v1/email-config", headers=auth_headers(token), json={
        "email_address": "s@example.com",
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "s@example.com",
        "password": "pass",
        "security_type": "STARTTLS",
    })
    resp = await client.put("/api/v1/email-config", headers=auth_headers(token), json={
        "smtp_host": "smtp.newhost.com",
    })
    assert resp.status_code == 200
    assert resp.json()["smtp_host"] == "smtp.newhost.com"


@pytest.mark.asyncio
async def test_email_config_isolation(client: AsyncClient):
    token_a = await setup_company(client, "isola@example.com")
    token_b = await setup_company(client, "isolb@example.com")

    await client.post("/api/v1/email-config", headers=auth_headers(token_a), json={
        "email_address": "a@example.com",
        "smtp_host": "smtp-a.com",
        "smtp_port": 587,
        "username": "a",
        "password": "pass",
        "security_type": "NONE",
    })
    await client.post("/api/v1/email-config", headers=auth_headers(token_b), json={
        "email_address": "b@example.com",
        "smtp_host": "smtp-b.com",
        "smtp_port": 465,
        "username": "b",
        "password": "pass",
        "security_type": "SSL_TLS",
    })

    resp_a = await client.get("/api/v1/email-config", headers=auth_headers(token_a))
    resp_b = await client.get("/api/v1/email-config", headers=auth_headers(token_b))

    assert resp_a.json()["smtp_host"] == "smtp-a.com"
    assert resp_b.json()["smtp_host"] == "smtp-b.com"
