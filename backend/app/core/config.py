"""
File with environment variables and general configuration logic.
`SECRET_KEY`, `ENVIRONMENT` etc. map to env variables with the same names.

Pydantic priority ordering:

1. (Most important, will overwrite everything) - environment variables
2. `.env` file in root folder of project
3. Default values

For project name, version, description we use pyproject.toml
For the rest, we use file `.env` (gitignored), see `.env.example`

`DEFAULT_SQLALCHEMY_DATABASE_URI` and `TEST_SQLALCHEMY_DATABASE_URI`:
Both are ment to be validated at the runtime, do not change unless you know
what are you doing. All the two validators do is to build full URI (TCP protocol)
to databases to avoid typo bugs.

See https://pydantic-docs.helpmanual.io/usage/settings/
"""

from pathlib import Path
from typing import Dict, List, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, validator

class Settings(BaseSettings):
    # CORE SETTINGS
    ENVIRONMENT: str
    
    # AUTHENTICATION
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24h TODO: place in env
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320 # 1 month TODO: place in env
    JWT_ALGORITHM: str = "HS256"
    
    # DATABASE PRODUCTION
    DEFAULT_DATABASE_HOSTNAME: str = "" # TODO: place var in env
    # DEFAULT_DATABASE_USER: str
    # DEFAULT_DATABASE_PASSWORD: str
    # DEFAULT_DATABASE_PORT: str
    DEFAULT_DATABASE_DB: str = "./app/snakemon.db" # TODO: place var in env
    DEFAULT_SQLALCHEMY_DATABASE_URI: str = ""
    # Builds: "sqlite+aiosqlite:///./app/snakemon.db"
    # later: "postgresql://user:password@postgresserver/db"
    
    # VALIDATORS
    @validator("DEFAULT_SQLALCHEMY_DATABASE_URI")
    def _assemble_default_db_connection(cls, v: str, values: Dict[str, str]) -> str:
        return AnyUrl.build(
            # scheme="postgresql+asyncpg", # postgres
            scheme="sqlite+aiosqlite", # sqlite
            # user=values["DEFAULT_DATABASE_USER"],
            # password=values["DEFAULT_DATABASE_PASSWORD"],
            host=values["DEFAULT_DATABASE_HOSTNAME"],
            # port=values["DEFAULT_DATABASE_PORT"],
            path=f"/{values['DEFAULT_DATABASE_DB']}",
        )
    
    class Config:
        env_file = '.env' # TODO: get from other config to use dev or prod
        case_sensitive = True
        
settings: Settings = Settings()
