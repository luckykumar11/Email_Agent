import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login, auth_headers
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


def test_password_hashing():
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_token():
    token = create_access_token(data={"sub": "123"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "123"


def test_jwt_invalid_token():
    payload = decode_access_token("invalid.token.here")
    assert payload is None


def test_jwt_expired_token():
    from datetime import timedelta
    token = create_access_token(data={"sub": "123"}, expires_delta=timedelta(seconds=-1))
    payload = decode_access_token(token)
    assert payload is None


@pytest.mark.asyncio
async def test_no_password_in_api_response(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "name": "Security Test",
        "email": "security@example.com",
        "password": "mypassword",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "security@example.com",
        "password": "mypassword",
    })
    user_data = resp.json()["user"]
    assert "password" not in user_data
    assert "password_hash" not in user_data


@pytest.mark.asyncio
async def test_cross_company_access_denied(client: AsyncClient):
    token_a = await register_and_login(client, "isolation1@example.com")
    token_b = await register_and_login(client, "isolation2@example.com")

    await client.post("/api/v1/company", headers=auth_headers(token_a), json={"name": "Co A"})
    await client.post("/api/v1/company", headers=auth_headers(token_b), json={"name": "Co B"})

    resp_a = await client.get("/api/v1/company", headers=auth_headers(token_a))
    resp_b = await client.get("/api/v1/company", headers=auth_headers(token_b))

    assert resp_a.json()["name"] == "Co A"
    assert resp_b.json()["name"] == "Co B"
    assert resp_a.json()["name"] != resp_b.json()["name"]


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    resp = await client.post("/api/v1/company", json={"name": "Hack"})
    assert resp.status_code in [401, 403]
