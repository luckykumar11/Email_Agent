import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login, auth_headers


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    resp = await client.post("/api/v1/auth/register", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "securepass123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["user"]["name"] == "John Doe"
    assert data["user"]["email"] == "john@example.com"
    assert "password" not in data["user"]


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "name": "John",
        "email": "dup@example.com",
        "password": "pass123",
    })
    resp = await client.post("/api/v1/auth/register", json={
        "name": "John2",
        "email": "dup@example.com",
        "password": "pass123",
    })
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "name": "Login User",
        "email": "login@example.com",
        "password": "pass123",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "pass123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "name": "Test",
        "email": "invalid@example.com",
        "password": "correctpass",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "invalid@example.com",
        "password": "wrongpass",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    resp = await client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "pass",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_endpoint(client: AsyncClient):
    token = await register_and_login(client, "me@example.com")
    resp = await client.get("/api/v1/auth/me", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_me_no_token(client: AsyncClient):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code in [401, 403]


@pytest.mark.asyncio
async def test_me_invalid_token(client: AsyncClient):
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_register_validation(client: AsyncClient):
    resp = await client.post("/api/v1/auth/register", json={
        "name": "Test",
        "email": "not-an-email",
        "password": "pass",
    })
    assert resp.status_code == 422
