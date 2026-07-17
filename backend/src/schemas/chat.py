"""Chat schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.models.chats import LLMModel
from src.schemas.base import Base
from src.settings import settings


class CreateChatRequest(BaseModel):
    """Create chat request schema."""

    title: str
    llm_model: LLMModel = settings.llm_settings.LLM_DEFAULT_FREE_MODEL


class CreateChatResponse(Base):
    """Create chat response schema."""

    id: UUID
    user_id: UUID
    title: str
    llm_model: LLMModel
    created_at: datetime


class RenameChatRequest(BaseModel):
    """Rename chat request schema."""

    title: str


class RenameChatResponse(CreateChatResponse):
    """Rename chat response schema."""


class DeleteChatResponse(CreateChatResponse):
    """Delete chat response schema."""


class GetChatResponse(CreateChatResponse):
    """Get chat response schema."""
