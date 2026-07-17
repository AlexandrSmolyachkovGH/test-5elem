"""Base schema."""

from pydantic import (
    BaseModel,
    ConfigDict,
)


class Base(BaseModel):
    """Base schema."""

    model_config = ConfigDict(
        from_attributes=True,
    )
