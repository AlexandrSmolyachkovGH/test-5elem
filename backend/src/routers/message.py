"""Message Router."""

from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Path,
    Depends,
    status,
)
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sqlite_handler import get_lite_session
from src.dependencies.auth import get_current_user
from src.schemas.message import (
    ClientMessageRequest,
    GetClientMessageResponse,
)
from src.services.message import message_service

message_router = APIRouter(
    prefix="/chats/{chat_id}/messages",
    tags=["messages"],
)


@message_router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_message(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    user_id: Annotated[UUID, Depends(get_current_user)],
    chat_id: Annotated[UUID, Path(...)],
    client_message: Annotated[ClientMessageRequest, Body(...)],
):
    """Create new message."""
    return StreamingResponse(
        content=message_service.send_message(
            session=session,
            user_id=user_id,
            chat_id=chat_id,
            client_message=client_message,
        ),
        status_code=status.HTTP_200_OK,
        media_type="text/plain",
    )


@message_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[GetClientMessageResponse],
)
async def get_messages(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    user_id: Annotated[UUID, Depends(get_current_user)],
    chat_id: Annotated[UUID, Path(...)],
):
    """Get all chat messages."""
    message_history = await message_service.get_all_messages(
        session=session,
        chat_id=chat_id,
        user_id=user_id,
    )

    return [
        GetClientMessageResponse.model_validate(message)
        for message in reversed(message_history)
    ]
