"""Exception handlers."""

from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse

from src.exceptions.custom_exceptions import (
    NotFoundErr,
    ServiceErr,
    TokenErr,
    LLMException,
)


async def process_token_error(
    request: Request,
    exc: TokenErr,
) -> JSONResponse:
    """Process token errors."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


async def process_not_found(
    request: Request,
    exc: NotFoundErr,
) -> JSONResponse:
    """Process not found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def process_service_error(
    request: Request,
    exc: ServiceErr,
) -> JSONResponse:
    """Process service errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def process_llm_error(
    request: Request,
    exc: LLMException,
) -> JSONResponse:
    """Process LLM errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )
