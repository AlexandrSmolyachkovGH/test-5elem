"""Main backend entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from src.db.sqlite_handler import SqliteHandler
from src.routers.auth import auth_router
from src.routers.chat import chat_router
from src.routers.message import message_router
from src.exceptions.custom_exceptions import (
    TokenErr,
    NotFoundErr,
    ServiceErr,
)
from src.exceptions.exception_handlers import (
    process_token_error,
    process_not_found,
    process_service_error,
)
from src.settings import settings


@asynccontextmanager
async def lifespan(
    _app: FastAPI,
) -> AsyncGenerator[None, None]:
    """Lifespan context manager."""
    lite = SqliteHandler()
    _app.state.db = lite

    try:
        yield

    finally:
        await lite.dispose()


app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=settings.general.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(message_router, prefix="/api")

app.add_exception_handler(TokenErr, process_token_error)  # noqa
app.add_exception_handler(NotFoundErr, process_not_found)  # noqa
app.add_exception_handler(ServiceErr, process_service_error)  # noqa

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
