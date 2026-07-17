"""Auth dependency."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from src.utils.jwt_handler import jwt_handler

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
) -> UUID:
    """Extract user_id from token."""

    token = credentials.credentials
    user_id = jwt_handler.verify_access_token(
        token=token,
    )

    return user_id
