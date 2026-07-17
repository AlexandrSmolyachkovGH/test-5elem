"""Auth repository."""

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.decorators import repo_error_decor
from src.models.users import User


class AuthRepository:
    """Auth repository."""

    @repo_error_decor
    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[User]:
        """Retrieve all users."""
        stmt = select(User)
        users = await session.execute(stmt)

        return list(users.scalars())

    @repo_error_decor
    async def create_user(
        self,
        session: AsyncSession,
        username: str,
        hashed_password: str,
    ) -> User:
        """Create new user."""
        new_user = User(
            username=username,
            hashed_password=hashed_password,
        )
        session.add(new_user)
        await session.flush()

        return new_user

    @repo_error_decor
    async def get_user(
        self,
        session: AsyncSession,
        username: str,
    ) -> User | None:
        """Get user."""
        stmt = select(User).where(User.username == username)
        user = await session.execute(stmt)

        return user.scalar_one_or_none()


auth_repository: AuthRepository = AuthRepository()
