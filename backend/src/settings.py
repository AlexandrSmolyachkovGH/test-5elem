"""Project settings."""

from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parents[2]


class BaseConf(BaseSettings):
    """Base settings class."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class DBSettings(BaseConf):
    """Database settings class."""

    DB_ECHO: bool = True
    DB_NAME: str = "new.db"

    @property
    def db_url(self) -> str:
        """Database connection string."""
        return f"sqlite+aiosqlite:///src/{self.DB_NAME}"


class LLMSettings(BaseConf):
    """LLM settings class."""

    LLM_API_KEY: str
    LLM_DEFAULT_FREE_MODEL: str
    LLM_PROVIDER: str = "openrouter"
    LLM_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    CHUNK_SIZE: int = 1024
    LLM_CONNECT_TIMEOUT: int = 5
    LLM_READ_TIMEOUT: int = 30
    LLM_WRITE_TIMEOUT: int = 10
    LLM_POOL_TIMEOUT: int = 10


class JWTSettings(BaseConf):
    """JWT settings class."""

    JWT_SECRET: SecretStr
    JWT_ALGORITHM: SecretStr
    JWT_EXP_MINUTES: int = 60


class GeneralSettings(BaseConf):
    """General settings class."""

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
        "http://localhost",
        "http://localhost:80",
    ]


class MainSettings:
    """Main settings class."""

    def __init__(self) -> None:
        """Init main settings."""
        self.db_settings = DBSettings()
        self.llm_settings = LLMSettings()
        self.jwt_settings = JWTSettings()
        self.general = GeneralSettings()


settings = MainSettings()
