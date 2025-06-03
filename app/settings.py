from pydantic_settings import BaseSettings
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()



class Settings(BaseSettings) :
    DATABASE_TYPE : str = os.getenv('DATABASE_TYPE', 'sqlite')
    DATABASE_NAME : str  = os.getenv('DATABASE_NAME', '')
    DATABASE_USERNAME : str = os.getenv('DATABASE_USERNAME', '')
    DATABASE_PASSWORD : str = os.getenv('DATABASE_PASSWORD' , '')
    DATABASE_PORT : int = int(os.getenv('DATABASE_PORT', 0))
    DATABASE_HOST : str = os.getenv('DATABASE_HOST', 'localhost')
    SQLITE_URL: str = f"sqlite:///./db.sqlite3"
    SECRET_KEY : str = os.getenv('SECRET_KEY', '')
    ALGORITHM : str = os.getenv('ALGORITHM','HS256')
    ACCESS_TOKEN_LIFETIME : timedelta = timedelta(minutes = 10)
    REFRESH_TOKEN_LIFETIME : timedelta = timedelta(days = 3)
    ROTATE_REFRESH_TOKENS : bool = True
    BLACKLIST_ON_ROTATION : bool = True
    STATIC_FILES : str = '/static'
settings = Settings()

