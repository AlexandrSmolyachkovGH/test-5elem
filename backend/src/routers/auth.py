"""Auth router module."""

from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
    Body,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sqlite_handler import get_lite_session
from src.exceptions.custom_exceptions import (
    ManualNotFoundErr,
    ManualServiceErr,
)
from src.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RegisterResponse,
    LoginResponse,
)
from src.services.auth import auth_service

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
)
async def register(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    register_data: Annotated[RegisterRequest, Body(...)],
) -> RegisterResponse:
    """Register user."""
    try:
        new_user = await auth_service.create_user(
            session=session,
            register_data=register_data,
        )

        return RegisterResponse.model_validate(new_user)

    except ManualServiceErr as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def login(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
    login_data: Annotated[LoginRequest, Body(...)],
) -> LoginResponse:
    """Login user. Return access token."""
    try:
        token = await auth_service.login(
            session=session,
            login_data=login_data,
        )

        return LoginResponse(
            access_token=token,
        )

    except ManualNotFoundErr as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
        )


@auth_router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=list[RegisterResponse],
)
async def get_users(
    session: Annotated[AsyncSession, Depends(get_lite_session)],
):
    """Get users."""
    users = await auth_service.get_users(
        session=session,
    )

    return [RegisterResponse.model_validate(user) for user in users]
