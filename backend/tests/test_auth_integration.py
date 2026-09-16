def test_register_creates_user_and_returns_tokens(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "Password123",
            "full_name": "New User",
            "organization_name": "New Org",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_register_fails_with_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123",
        "full_name": "User One",
        "organization_name": "Org One",
    }
    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400


def test_login_succeeds_with_correct_credentials(client):
    client.post(
        "/auth/register",
        json={
            "email": "logintest@example.com",
            "password": "Password123",
            "full_name": "Login Test",
            "organization_name": "Login Org",
        },
    )

    response = client.post(
        "/auth/login",
        json={"email": "logintest@example.com", "password": "Password123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fails_with_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "Password123",
            "full_name": "Wrong Pass",
            "organization_name": "Wrong Org",
        },
    )

    response = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "IncorrectPassword"},
    )

    assert response.status_code == 401


def test_protected_endpoint_requires_authentication(client):
    response = client.get("/customers")
    assert response.status_code == 401


def test_protected_endpoint_works_with_valid_token(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "protected@example.com",
            "password": "Password123",
            "full_name": "Protected Test",
            "organization_name": "Protected Org",
        },
    )
    token = register_response.json()["access_token"]

    response = client.get(
        "/customers", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []