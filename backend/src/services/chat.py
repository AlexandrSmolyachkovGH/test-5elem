"""Chat service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.custom_exceptions import (
    ServiceErr,
    NotFoundErr,
    RepositoryErr,
)
from src.models import Chat
from src.repositories.chat import chat_repository
from src.schemas.chat import (
    CreateChatRequest,
    RenameChatRequest,
)


class ChatService:
    """Chat service."""

    async def create_chat(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_data: CreateChatRequest,
    ) -> Chat:
        """Create new chat."""
        try:
            async with session.begin():
                chat = await chat_repository.create_chat(
                    session=session,
                    user_id=user_id,
                    title=chat_data.title,
                    llm_model=chat_data.llm_model,
                )

                return chat

        except RepositoryErr as err:
            raise ServiceErr(err) from err

    async def get_chat(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_id: UUID,
    ) -> Chat:
        """Get chat by id."""
        try:
            chat = await chat_repository.get_chat(
                session=session,
                chat_id=chat_id,
                user_id=user_id,
            )

            if chat is None:
                msg = (
                    f"Chat with id {chat_id} and "
                    f"owner {user_id} was not found."
                )
                raise NotFoundErr(msg)

            return chat

        except RepositoryErr as err:
            raise ServiceErr(err) from err

    async def get_chats(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> list[Chat]:
        """Get all user's chats."""
        try:
            chats = await chat_repository.get_chats(
                session=session,
                user_id=user_id,
            )

            return chats

        except RepositoryErr as err:
            raise ServiceErr(err) from err

    async def update_chat(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_id: UUID,
        update_data: RenameChatRequest,
    ) -> Chat:
        """Rename chat."""
        try:
            async with session.begin():
                chat = await chat_repository.rename_chat(
                    session=session,
                    user_id=user_id,
                    chat_id=chat_id,
                    title=update_data.title,
                )

                if chat is None:
                    msg = (
                        f"Chat with id: {chat_id} and "
                        f"owner {user_id} was not found and "
                        f"was not updated."
                    )
                    raise NotFoundErr(msg)

                return chat

        except RepositoryErr as err:
            raise ServiceErr(err) from err

    async def delete_chat(
        self,
        session: AsyncSession,
        user_id: UUID,
        chat_id: UUID,
    ) -> Chat:
        """Delete chat."""
        try:
            async with session.begin():
                chat = await chat_repository.delete_chat(
                    session=session,
                    user_id=user_id,
                    chat_id=chat_id,
                )

                if chat is None:
                    msg = (
                        f"Chat with id: {chat_id} and "
                        f"owner {user_id} was not found and "
                        f"was not deleted."
                    )
                    raise NotFoundErr(msg)

                return chat

        except RepositoryErr as err:
            raise ServiceErr(err) from err


chat_service: ChatService = ChatService()
