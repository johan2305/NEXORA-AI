from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.core.config import get_settings


settings = get_settings()


class Base(DeclarativeBase):
    """
    Base class for all NEXORA ORM models.
    """

    pass


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=1800,
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for an application request.

    The session is always closed after the request finishes.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()