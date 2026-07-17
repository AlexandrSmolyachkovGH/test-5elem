"""JWT Handler."""

from datetime import (
    datetime,
    timedelta,
    timezone,
)
from uuid import UUID

import jwt

from src.exceptions.custom_exceptions import TokenErr
from src.settings import settings


class JWTHandler:

    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        """Create an access token."""
        token = jwt.encode(
            payload={
                "sub": str(user_id),
                "exp": datetime.now(timezone.utc)
                + timedelta(
                    minutes=settings.jwt_settings.JWT_EXP_MINUTES,
                ),
            },
            key=settings.jwt_settings.JWT_SECRET.get_secret_value(),
            algorithm=settings.jwt_settings.JWT_ALGORITHM.get_secret_value(),
        )

        return token

    def verify_access_token(
        self,
        token: str,
    ) -> UUID:
        """
        Verify an access token.
        Return sub UUID.
        """
        try:
            token = jwt.decode(
                jwt=token,
                key=settings.jwt_settings.JWT_SECRET.get_secret_value(),
                algorithms=[
                    settings.jwt_settings.JWT_ALGORITHM.get_secret_value(),
                ],
            )

            return UUID(token["sub"])

        except jwt.InvalidTokenError as err:
            raise TokenErr(
                "Invalid or expired token. Please log in again."
            ) from err


jwt_handler: JWTHandler = JWTHandler()
