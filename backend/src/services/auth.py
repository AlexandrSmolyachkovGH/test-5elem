"""Auth Service."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.custom_exceptions import (
    RepositoryErr,
    ServiceErr,
    ManualServiceErr,
    ManualNotFoundErr,
)
from src.models.users import User
from src.repositories.auth import auth_repository
from src.schemas.auth import (
    RegisterRequest,
    LoginRequest,
)
from src.utils.pwd_hashing import pwd_handler
from src.utils.jwt_handler import jwt_handler


class AuthService:
    """Auth Service."""

    async def get_users(
        self,
        session: AsyncSession,
    ) -> list[User]:
        """Retrieve all users."""
        try:
            users = await auth_repository.get_all_users(
                session=session,
            )

            return users
        except RepositoryErr as err:
            raise ServiceErr(err) from err

    async def create_user(
        self,
        session: AsyncSession,
        register_data: RegisterRequest,
    ) -> User:
        """Create a new user."""
        try:
            async with session.begin():
                hashed_password = pwd_handler.get_password_hash(
                    password=register_data.password,
                )
                new_user = await auth_repository.create_user(
                    session=session,
                    username=register_data.username,
                    hashed_password=hashed_password,
                )

                return new_user

        except RepositoryErr as err:
            raise ManualServiceErr(err) from err

    async def login(
        self,
        session: AsyncSession,
        login_data: LoginRequest,
    ) -> str:
        """
        Login user.
        Get user from DB. Verify user password.
        Return access token.
        """
        try:
            user = await auth_repository.get_user(
                session=session, username=login_data.username
            )

            if user is None:
                raise ManualNotFoundErr(
                    f"User with username {login_data.username} not found",
                )

            pwd_check = pwd_handler.check_password(
                password=login_data.password,
                hashed_password=user.hashed_password,
            )

            if not pwd_check:
                raise ManualServiceErr(
                    f"Incorrect password for user {login_data.username}.",
                )

            token = jwt_handler.create_access_token(
                user_id=user.id,
            )
            return token

        except RepositoryErr as err:
            raise ServiceErr(err) from err


auth_service: AuthService = AuthService()
