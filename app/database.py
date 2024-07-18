from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.configs import AppSettings

settings = AppSettings()

DATABASE_URL = settings.postgres_url

engie = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engie)
Base = declarative_base()
