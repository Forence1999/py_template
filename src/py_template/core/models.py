"""Core data models for py_template."""

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """Base model for all data structures."""

    model_config = {
        "validate_assignment": True,
        "arbitrary_types_allowed": False,
    }
