"""
py_template - A minimal Python project template.

This package provides a template structure for Python projects with modern tooling.
"""

from py_template.__version__ import __version__
from py_template.core.exceptions import ServiceError, TemplateError, ValidationError
from py_template.core.models import BaseModel
from py_template.services import BaseService

# Public API exports
__all__ = [
    "__version__",
    "TemplateError",
    "ValidationError",
    "ServiceError",
    "BaseModel",
    "BaseService",
]
