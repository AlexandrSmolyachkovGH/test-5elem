"""Custom exceptions."""


class RepositoryErr(Exception):
    """Custom error class for repository layer."""


class ServiceErr(Exception):
    """Custom error class for service layer."""


class NotFoundErr(ServiceErr):
    """Custom error class for not found errors."""


class ManualNotFoundErr(NotFoundErr):
    """Service layer error class for manual not found errors handling."""


class ManualServiceErr(ServiceErr):
    """Service layer error class for manual handling service errors."""


class TokenErr(Exception):
    """Custom error class for token errors catching."""


class LLMException(Exception):
    """Custom error class for LLM exceptions catching."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        """Init LLMException."""
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code

    def __str__(self) -> str:
        """String representation of LLMException."""
        code = self.code or "Unknown"
        status = self.status_code or "Unknown"

        return (
            f"LLMException: {self.message}. "
            f"Error code: {code}. "
            f"Error status code: {status}."
        )
