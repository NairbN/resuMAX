from app.db.session import Base, engine  # noqa: F401
import app.models  # noqa: F401


def init_db():
    """
    For local/dev environments where Alembic isn't run, ensure tables exist.
    In staging/prod, prefer Alembic migrations.
    """
    Base.metadata.create_all(bind=engine)
