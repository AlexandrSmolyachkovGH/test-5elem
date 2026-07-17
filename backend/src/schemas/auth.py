"""Auth schemas."""

from uuid import UUID

from pydantic import BaseModel

from src.schemas.base import Base


class RegisterRequest(BaseModel):
    """Register request schema."""

    username: str
    password: str


class RegisterResponse(Base):
    """Register response schema."""

    id: UUID
    username: str


class LoginRequest(BaseModel):
    """Login request schema."""

    username: str
    password: str


class LoginResponse(Base):
    """Login response schema."""

    access_token: str
    token_type: str = "bearer"
