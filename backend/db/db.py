from __future__ import annotations

from sqlmodel import Session, SQLModel, create_engine, select

from backend.core.settings import get_settings

settings = get_settings()
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    import backend.db.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    _seed_default_tenant()
    from backend.db.seed import seed_all

    seed_all()


def _seed_default_tenant() -> None:
    from backend.db.models import Tenant

    with Session(engine) as session:
        existing = session.exec(
            select(Tenant).where(Tenant.id == settings.default_tenant_id)
        ).first()
        if existing is None:
            session.add(Tenant(id=settings.default_tenant_id, name="default"))
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session
