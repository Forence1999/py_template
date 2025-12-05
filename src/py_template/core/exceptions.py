"""Custom exceptions for py_template."""


class TemplateError(Exception):
    """Base exception for all template errors."""


class ValidationError(TemplateError):
    """Raised when data validation fails."""


class ServiceError(TemplateError):
    """Raised when service execution fails."""
