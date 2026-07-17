"""Message models."""

from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as SA_UUID,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base import Base
from src.models.mixins import (
    UUIDPkMixin,
    CreatedAtMixin,
)

if TYPE_CHECKING:
    from src.models.chats import Chat


class MessageRole(StrEnum):
    """Message role."""

    USER = "user"
    ASSISTANT = "assistant"


class Message(UUIDPkMixin, CreatedAtMixin, Base):
    """Message model."""

    __tablename__ = "messages"

    chat_id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey(
            "chats.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    chat: Mapped["Chat"] = relationship(
        "Chat",
        back_populates="messages",
    )
