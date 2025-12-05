"""Test custom exceptions."""

import pytest

from py_template import ServiceError, TemplateError, ValidationError


def test_template_error():
    """Test base TemplateError."""
    with pytest.raises(TemplateError):
        raise TemplateError("Test error")


def test_validation_error():
    """Test ValidationError."""
    with pytest.raises(ValidationError):
        raise ValidationError("Validation failed")


def test_service_error():
    """Test ServiceError."""
    with pytest.raises(ServiceError):
        raise ServiceError("Service failed")


def test_exception_hierarchy():
    """Test exception hierarchy."""
    assert issubclass(ValidationError, TemplateError)
    assert issubclass(ServiceError, TemplateError)
