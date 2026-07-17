"""Chat repository."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    update,
    delete,
)

from src.models import Chat
from src.models.chats import LLMModel
from src.exceptions.decorators import repo_error_decor


class ChatRepository:
    """Chat repository."""

    @repo_error_decor
    async def create_chat(
        self,
        session: AsyncSession,
        user_id: UUID,
        title: str,
        llm_model: LLMModel,
    ) -> Chat:
        """Create new chat."""

        new_chat = Chat(
            user_id=user_id,
            title=title,
            llm_model=llm_model,
        )
        session.add(new_chat)
        await session.flush()

        return new_chat

    @repo_error_decor
    async def get_chat(
        self,
        session: AsyncSession,
        chat_id: UUID,
        user_id: UUID,
    ) -> Chat | None:
        """Get chat."""
        stmt = select(Chat).where(
            Chat.id == chat_id,
            Chat.user_id == user_id,
        )
        chat = await session.execute(stmt)

        return chat.scalar_one_or_none()

    @repo_error_decor
    async def get_chats(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> list[Chat]:
        """Get chats."""
        stmt = select(Chat).where(Chat.user_id == user_id)
        chats = await session.execute(stmt)

        return list(chats.scalars())

    @repo_error_decor
    async def rename_chat(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_id: UUID,
        title: str,
    ) -> Chat | None:
        """Rename chat."""
        stmt = (
            update(Chat)
            .where(
                Chat.id == chat_id,
                Chat.user_id == user_id,
            )
            .values(title=title)
            .returning(Chat)
        )
        chat = await session.execute(stmt)

        return chat.scalar_one_or_none()

    @repo_error_decor
    async def delete_chat(
        self,
        session: AsyncSession,
        chat_id: UUID,
        user_id: UUID,
    ) -> Chat | None:
        """Delete chat."""
        stmt = (
            delete(Chat)
            .where(
                Chat.id == chat_id,
                Chat.user_id == user_id,
            )
            .returning(Chat)
        )
        chat = await session.execute(stmt)
        return chat.scalar_one_or_none()


chat_repository: ChatRepository = ChatRepository()
