import os

from pydantic.v1 import BaseConfig

from dotenv import load_dotenv


load_dotenv()


class Settings(BaseConfig):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    API_VERSION: str = os.getenv("API_VERSION")
    REQUEST_PER_MINUTES: int = os.getenv("REQUEST_PER_MINUTES")
    REQUEST_PER_MINUTES_AUTH: int = os.getenv("REQUEST_PER_MINUTES_AUTH")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True


settings: Settings = Settings() 
