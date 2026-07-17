"""Message service."""

from typing import AsyncIterator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.custom_exceptions import (
    ServiceErr,
    RepositoryErr,
    LLMException,
)
from src.llm.openrouter_client import openrouter_client
from src.models import Chat
from src.models.messages import (
    MessageRole,
    Message,
)
from src.repositories.chat import chat_repository
from src.repositories.message import message_repository
from src.schemas.message import ClientMessageRequest


class MessageService:
    """Message service."""

    async def _check_user_is_chat_owner(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_id: UUID,
    ) -> Chat:
        """Check if user is chat owner."""
        try:
            chat = await chat_repository.get_chat(
                session=session,
                chat_id=chat_id,
                user_id=user_id,
            )

            if not chat:
                raise ServiceErr("User is not chat owner.")

            return chat
        except RepositoryErr as err:
            raise ServiceErr(err) from err

    async def _write_message_to_db(
        self,
        session: AsyncSession,
        chat_id: UUID,
        content: str,
        role: MessageRole,
    ) -> Message:
        """Write message to database."""
        message = await message_repository.create_message(
            session=session,
            chat_id=chat_id,
            content=content,
            role=role,
        )
        await session.commit()
        return message

    async def get_all_messages(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_id: UUID,
    ) -> list[Message]:
        """Get all messages."""
        await self._check_user_is_chat_owner(
            session=session,
            user_id=user_id,
            chat_id=chat_id,
        )
        try:
            messages = await message_repository.get_messages(
                session=session,
                chat_id=chat_id,
                limit=None,
            )
            return messages

        except RepositoryErr as err:
            raise ServiceErr(err) from err

    async def send_message(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_id: UUID,
        client_message: ClientMessageRequest,
    ) -> AsyncIterator[str]:
        """
        Ask chat.
        Receive chat message.
        Store chat history to database.
        """
        chat = await self._check_user_is_chat_owner(
            session=session,
            user_id=user_id,
            chat_id=chat_id,
        )
        try:
            await self._write_message_to_db(
                session=session,
                chat_id=chat_id,
                content=client_message.content,
                role=MessageRole.USER,
            )
            await session.commit()

        except RepositoryErr as err:
            await session.rollback()
            raise ServiceErr(err) from err

        chat_history = await message_repository.get_messages(
            session=session,
            chat_id=chat_id,
        )

        answer = ""
        try:
            async for text_part in openrouter_client.stream_chat(
                model=chat.llm_model,
                messages=chat_history,
            ):
                answer += text_part
                yield text_part

        except LLMException as err:
            raise ServiceErr(err) from err

        try:
            await self._write_message_to_db(
                session=session,
                chat_id=chat_id,
                content=answer,
                role=MessageRole.ASSISTANT,
            )
            await session.commit()
        except RepositoryErr as err:
            await session.rollback()
            raise ServiceErr(err) from err


message_service: MessageService = MessageService()
