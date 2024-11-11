from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , scoped_session
from .settings import settings
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent


match settings.DATABASE_TYPE:

    case 'sqlite' :
        DATABASE_URL = F"{settings.SQLITE_URL}"
    case 'postgresql' : 
        DATABASE_URL = f"postgresql+psycopg2://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    case 'mysql' :
        DATABASE_URL = f"mysql+mysqldb://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    case _ :
        raise ValueError('Invalid setting on database Type')
    
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


