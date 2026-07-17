"""Message schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.models.messages import MessageRole
from src.schemas.base import Base


class ClientMessageRequest(BaseModel):
    """Client message request schema."""

    content: str


class GetClientMessageResponse(Base):
    """Client message response schema."""

    id: UUID
    content: str
    role: MessageRole
    created_at: datetime
