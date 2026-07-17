"""Chat routers."""

from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Path,
    Response,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sqlite_handler import get_lite_session
from src.dependencies.auth import get_current_user
from src.schemas.chat import (
    CreateChatRequest,
    CreateChatResponse,
    GetChatResponse,
    RenameChatRequest,
    RenameChatResponse,
)
from src.services.chat import chat_service

chat_router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)


@chat_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateChatResponse,
)
async def create_chat(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    user_id: Annotated[UUID, Depends(get_current_user)],
    chat_data: Annotated[CreateChatRequest, Body(...)],
):
    """Create new chat for the user."""
    chat = await chat_service.create_chat(
        session=session,
        user_id=user_id,
        chat_data=chat_data,
    )

    return CreateChatResponse.model_validate(chat)


@chat_router.get(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetChatResponse,
)
async def get_chat(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    user_id: Annotated[UUID, Depends(get_current_user)],
    chat_id: Annotated[UUID, Path(...)],
):
    """Get chat for the user by id."""
    chat = await chat_service.get_chat(
        session=session,
        user_id=user_id,
        chat_id=chat_id,
    )

    return GetChatResponse.model_validate(chat)


@chat_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[GetChatResponse],
)
async def get_chats(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    user_id: Annotated[UUID, Depends(get_current_user)],
):
    """Get all chats for the user."""
    chats = await chat_service.get_chats(
        session=session,
        user_id=user_id,
    )
    return [GetChatResponse.model_validate(chat) for chat in chats]


@chat_router.patch(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=RenameChatResponse,
)
async def rename_chat(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    user_id: Annotated[UUID, Depends(get_current_user)],
    chat_id: Annotated[UUID, Path(...)],
    update_data: Annotated[RenameChatRequest, Body(...)],
):
    """Update chat for the user by id."""
    chat = await chat_service.update_chat(
        session=session,
        user_id=user_id,
        chat_id=chat_id,
        update_data=update_data,
    )

    return RenameChatResponse.model_validate(chat)


@chat_router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    user_id: Annotated[UUID, Depends(get_current_user)],
    chat_id: Annotated[UUID, Path(...)],
):
    """Delete chat for the user by id."""
    await chat_service.delete_chat(
        session=session,
        user_id=user_id,
        chat_id=chat_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
