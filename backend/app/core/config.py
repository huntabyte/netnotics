from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, HttpUrl, PostgresDsn, validator
from pydantic.networks import AnyHttpUrl

PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str
    SECURITY_BCRYPT_ROUNDS: int = 12
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320  # 28 days

    PROJECT_NAME: str = "netnotics"

    SENTRY_DSN: Optional[HttpUrl] = None

    API_PATH: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # The following variables need to be defined in environment

    TEST_DATABASE_URL: Optional[PostgresDsn]
    DATABASE_URL: PostgresDsn
    ASYNC_DATABASE_URL: Optional[PostgresDsn]

    @validator("DATABASE_URL", pre=True)
    def build_test_database_url(cls, v: Optional[str], values: Dict[str, Any]):
        """Overrides DATABASE_URL with TEST_DATABASE_URL in test environment."""
        if "pytest" in sys.modules:
            if not values.get("TEST_DATABASE_URL"):
                raise Exception(
                    "pytest detected, but TEST_DATABASE_URL is not set in environment"
                )
            return values["TEST_DATABASE_URL"]
        return v

    @validator("ASYNC_DATABASE_URL")
    def build_async_database_url(cls, v: Optional[str], values: Dict[str, Any]):
        """Builds ASYNC_DATABASE_URL from DATABASE_URL."""
        v = values["DATABASE_URL"]
        return v.replace("postgresql", "postgresql+asyncpg") if v else v

    SECRET_KEY: str
    #  END: required environment variables

    class Config:
        env_file = f"{PROJECT_DIR}/.env"


settings: Settings = Settings()  # type: ignore
