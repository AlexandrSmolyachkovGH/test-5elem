"""Decorators for catching exceptions."""

from functools import wraps
from typing import (
    Callable,
    Coroutine,
    Any,
)

from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)

from src.exceptions.custom_exceptions import RepositoryErr


def repo_error_decor[**P, T](
    func: Callable[P, Coroutine[Any, Any, T]],
) -> Callable[P, Coroutine[Any, Any, T]]:
    """Catch and process repository errors."""

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        """Apply error handling to repo method."""
        class_name = args[0].__class__.__name__ if args else "UnknownRepo"
        func_name = f"{class_name}.{func.__name__}"

        try:
            result = await func(*args, **kwargs)

            return result

        except IntegrityError as err:
            if "unique constraint" in str(err.orig).lower():
                raise RepositoryErr(
                    f"Data already exists error. Locate: {func_name}."
                ) from err
            else:
                raise RepositoryErr(
                    f"Data validation error. Locate: {func_name}."
                ) from err

        except SQLAlchemyError as err:
            raise RepositoryErr(
                f"Error on the database side. Locate: {func_name}."
            ) from err

    return wrapper
