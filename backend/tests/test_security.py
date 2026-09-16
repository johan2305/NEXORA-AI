from backend.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)


def test_hash_password_creates_different_hash_than_plain_text():
    hashed = hash_password("MyPassword123")
    assert hashed != "MyPassword123"


def test_verify_password_succeeds_with_correct_password():
    hashed = hash_password("MyPassword123")
    assert verify_password("MyPassword123", hashed) is True


def test_verify_password_fails_with_wrong_password():
    hashed = hash_password("MyPassword123")
    assert verify_password("WrongPassword", hashed) is False


def test_access_token_can_be_decoded():
    token = create_access_token({"sub": "user-123", "org": "org-456", "role": "org_admin"})
    payload = decode_token(token)

    assert payload is not None
    assert payload["sub"] == "user-123"
    assert payload["type"] == "access"


def test_refresh_token_has_correct_type():
    token = create_refresh_token({"sub": "user-123", "org": "org-456", "role": "org_admin"})
    payload = decode_token(token)

    assert payload["type"] == "refresh"


def test_decode_invalid_token_returns_none():
    payload = decode_token("this.is.not.a.valid.token")
    assert payload is None


def test_hash_token_is_deterministic():
    token = "some-refresh-token-value"
    assert hash_token(token) == hash_token(token)


def test_hash_token_differs_for_different_tokens():
    assert hash_token("token-a") != hash_token("token-b")