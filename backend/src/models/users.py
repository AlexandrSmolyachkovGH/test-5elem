"""User models."""

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
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


class User(UUIDPkMixin, CreatedAtMixin, Base):
    """User model."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    chats: Mapped[list["Chat"]] = relationship(
        "Chat",
        back_populates="user",
        passive_deletes=True,
    )
