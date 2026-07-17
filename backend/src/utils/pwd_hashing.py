"""Password hashing module."""

import bcrypt


class PasswordHandler:
    """Password handler."""

    def get_password_hash(
        self,
        password: str,
    ) -> str:
        """
        Hash a plain-text password.
        Return hashed string.
        """
        hashed: bytes = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        )
        hashed_str: str = hashed.decode("utf-8")

        return hashed_str

    def check_password(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:
        """
        Check password.
        Return True if password is correct, else False.
        """

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )


pwd_handler = PasswordHandler()
