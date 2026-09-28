import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from tests.conftest import register_and_login, auth_headers


async def setup_full(client: AsyncClient, email: str) -> str:
    token = await register_and_login(client, email)
    await client.post("/api/v1/company", headers=auth_headers(token), json={"name": "Send Co"})
    await client.post("/api/v1/email-config", headers=auth_headers(token), json={
        "email_address": "send@example.com",
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "send@example.com",
        "password": "pass",
        "security_type": "STARTTLS",
        "sender_name": "Send Co",
    })
    await client.post("/api/v1/signature", headers=auth_headers(token), json={
        "signature_text": "Best,\nSend Co",
        "enabled": True,
        "append_automatically": True,
    })
    return token


@pytest.mark.asyncio
@patch("app.services.email_service.send_smtp_email", return_value=(True, "Sent"))
async def test_send_email_success(mock_send, client: AsyncClient):
    token = await setup_full(client, "send1@example.com")
    resp = await client.post("/api/v1/emails/send", headers=auth_headers(token), json={
        "recipient": "recipient@example.com",
        "subject": "Hello",
        "body": "Test body",
        "format": "html",
    })
    assert resp.status_code == 200
    assert resp.json()["success"] is True


@pytest.mark.asyncio
@patch("app.services.email_service.send_smtp_email", return_value=(False, "SMTP error"))
async def test_send_email_failure(mock_send, client: AsyncClient):
    token = await setup_full(client, "send2@example.com")
    resp = await client.post("/api/v1/emails/send", headers=auth_headers(token), json={
        "recipient": "r@example.com",
        "subject": "Fail",
        "body": "Body",
    })
    assert resp.status_code == 200
    assert resp.json()["success"] is False


@pytest.mark.asyncio
@patch("app.services.email_service.send_smtp_email", return_value=(True, "Sent"))
async def test_email_history(mock_send, client: AsyncClient):
    token = await setup_full(client, "send3@example.com")
    await client.post("/api/v1/emails/send", headers=auth_headers(token), json={
        "recipient": "r@example.com",
        "subject": "Test",
        "body": "Body",
    })
    resp = await client.get("/api/v1/emails/history", headers=auth_headers(token))
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert data["emails"][0]["recipient"] == "r@example.com"


@pytest.mark.asyncio
async def test_email_history_isolation(client: AsyncClient):
    token_a = await setup_full(client, "hista@example.com")
    token_b = await setup_full(client, "histb@example.com")

    with patch("app.services.email_service.send_smtp_email", return_value=(True, "Sent")):
        await client.post("/api/v1/emails/send", headers=auth_headers(token_a), json={
            "recipient": "r@a.com", "subject": "A", "body": "A",
        })
        await client.post("/api/v1/emails/send", headers=auth_headers(token_b), json={
            "recipient": "r@b.com", "subject": "B", "body": "B",
        })

    hist_a = await client.get("/api/v1/emails/history", headers=auth_headers(token_a))
    hist_b = await client.get("/api/v1/emails/history", headers=auth_headers(token_b))

    assert hist_a.json()["total"] == 1
    assert hist_a.json()["emails"][0]["recipient"] == "r@a.com"
    assert hist_b.json()["total"] == 1
    assert hist_b.json()["emails"][0]["recipient"] == "r@b.com"
