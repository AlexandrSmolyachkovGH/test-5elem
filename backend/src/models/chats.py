"""Chat model."""

from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as SA_UUID,
    String,
    ForeignKey,
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
from src.settings import settings

if TYPE_CHECKING:
    from src.models.users import User
    from src.models.messages import Message


class LLMModel(StrEnum):
    DEFAULT_FREE = settings.llm_settings.LLM_DEFAULT_FREE_MODEL
    HY3 = "tencent/hunyuan-a13b-instruct:free"
    LAGUNA = "poolside/laguna-m.1:free"


class Chat(UUIDPkMixin, CreatedAtMixin, Base):
    """Chat model."""

    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    llm_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default=LLMModel.HY3.value,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="chats",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
    )
