from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.configs import AppSettings

settings = AppSettings()

DATABASE_URL = settings.postgres_url

engie = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engie)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
