import pytest
from pydantic import ValidationError

from backend.auth.schemas import RegisterRequest


def test_register_request_accepts_valid_password():
    data = RegisterRequest(
        email="user@example.com",
        password="Password123",
        full_name="Test User",
        organization_name="Test Org",
    )
    assert data.password == "Password123"


def test_register_request_rejects_password_without_uppercase():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="user@example.com",
            password="password123",
            full_name="Test User",
            organization_name="Test Org",
        )


def test_register_request_rejects_password_without_lowercase():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="user@example.com",
            password="PASSWORD123",
            full_name="Test User",
            organization_name="Test Org",
        )


def test_register_request_rejects_short_password():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="user@example.com",
            password="Pw1",
            full_name="Test User",
            organization_name="Test Org",
        )


def test_register_request_rejects_invalid_email():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="not-an-email",
            password="Password123",
            full_name="Test User",
            organization_name="Test Org",
        )