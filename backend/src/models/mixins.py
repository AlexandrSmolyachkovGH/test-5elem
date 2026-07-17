"""Mixin for SQLAlchemy models."""

from datetime import datetime
from uuid import (
    uuid7,
    UUID,
)

from sqlalchemy import (
    UUID as SA_UUID,
    DateTime,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class UUIDPkMixin:
    """Primary key UUID mixin."""

    id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )


class CreatedAtMixin:
    """Created at mixin."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
