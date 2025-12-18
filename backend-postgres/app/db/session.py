from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.pool import StaticPool

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _create_engine():
    url = settings.database_url

    # SQLite needs special handling (especially in-memory DBs for tests)
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        if ":memory:" in url:
            return create_engine(
                url,
                connect_args=connect_args,
                poolclass=StaticPool,
                future=True,
            )
        return create_engine(url, connect_args=connect_args, future=True)

    # Default (e.g., PostgreSQL)
    return create_engine(url, pool_pre_ping=True, future=True)


engine = _create_engine()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True, class_=Session)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
