"""Message repository."""

from uuid import UUID

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.messages import (
    MessageRole,
    Message,
)
from src.exceptions.decorators import repo_error_decor


class MessageRepository:
    """Message repository."""

    @repo_error_decor
    async def create_message(
        self,
        session: AsyncSession,
        chat_id: UUID,
        content: str,
        role: MessageRole,
    ) -> Message:
        """Create new message."""
        new_message = Message(
            chat_id=chat_id,
            content=content,
            role=role,
        )
        session.add(new_message)
        await session.flush()

        return new_message

    @repo_error_decor
    async def get_messages(
        self,
        session: AsyncSession,
        chat_id: UUID,
        limit: int | None = 20,
    ) -> list[Message]:
        """Get messages."""
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
        )
        if limit is not None:
            stmt = stmt.limit(limit)

        messages = await session.execute(stmt)

        return list(messages.scalars())


message_repository: MessageRepository = MessageRepository()
