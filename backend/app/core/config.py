import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fatemi Wirasat Engine"
    # Defaults to sqlite for local dev, overridable by environment variables
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./faraiz.db")

settings = Settings()
