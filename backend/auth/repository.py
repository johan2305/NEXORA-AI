import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.auth.models import RefreshToken


def store_refresh_token(
    db: Session, user_id: uuid.UUID, token_hash: str, expires_at: datetime
) -> RefreshToken:
    token = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    db.add(token)
    db.flush()
    return token


def get_valid_token(db: Session, token_hash: str) -> RefreshToken | None:
    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked.is_(False),
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )


def revoke_token(db: Session, token: RefreshToken) -> None:
    token.revoked = True
    db.flush()