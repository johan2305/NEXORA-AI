import re
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.auth import repository as auth_repository
from backend.auth.schemas import RegisterRequest, LoginRequest, TokenResponse
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_token,
)
from backend.organizations import repository as org_repository
from backend.users import repository as user_repository
from backend.audit import repository as audit_repository


class AuthError(Exception):
    pass


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or str(uuid.uuid4())[:8]


def register(db: Session, data: RegisterRequest) -> TokenResponse:
    if user_repository.get_by_email(db, data.email):
        raise AuthError("Email already registered")

    user = user_repository.create_user(
        db,
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    org = org_repository.create_organization(
        db, name=data.organization_name, slug=_slugify(data.organization_name)
    )
    org_repository.create_membership(
        db, user_id=user.id, organization_id=org.id, role="org_admin"
    )

    return _issue_tokens(db, user_id=user.id, organization_id=org.id, role="org_admin")


def login(db: Session, data: LoginRequest) -> TokenResponse:
    user = user_repository.get_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise AuthError("Invalid credentials")
    if not user.is_active:
        raise AuthError("User is inactive")

    membership = org_repository.get_first_membership_for_user(db, user.id)
    if not membership:
        raise AuthError("User has no organization")

    audit_repository.log(
        db,
        organization_id=membership.organization_id,
        action="LOGIN",
        resource_type="user",
        user_id=user.id,
    )

    return _issue_tokens(
        db, user_id=user.id, organization_id=membership.organization_id, role=membership.role
    )


def refresh(db: Session, refresh_token: str) -> TokenResponse:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise AuthError("Invalid refresh token")

    token_hash = hash_token(refresh_token)
    stored = auth_repository.get_valid_token(db, token_hash)
    if not stored:
        raise AuthError("Refresh token not recognized or expired")

    auth_repository.revoke_token(db, stored)

    user_id = uuid.UUID(payload["sub"])
    organization_id = uuid.UUID(payload["org"])
    role = payload["role"]

    return _issue_tokens(db, user_id=user_id, organization_id=organization_id, role=role)


def _issue_tokens(db: Session, user_id: uuid.UUID, organization_id: uuid.UUID, role: str) -> TokenResponse:
    token_data = {"sub": str(user_id), "org": str(organization_id), "role": role}

    access_token = create_access_token(token_data)
    refresh_token_value = create_refresh_token(token_data)

    payload = decode_token(refresh_token_value)
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    auth_repository.store_refresh_token(
        db,
        user_id=user_id,
        token_hash=hash_token(refresh_token_value),
        expires_at=expires_at,
    )

    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token_value)