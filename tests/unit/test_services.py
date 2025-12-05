"""Tests for service modules."""

import pytest

from py_template import BaseService, ServiceError


def test_base_service_is_abstract():
    """Test that BaseService cannot be instantiated directly."""
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        BaseService()


def test_base_service_requires_execute():
    """Test that concrete implementations must implement execute method."""

    class IncompleteService(BaseService):
        pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteService()


def test_concrete_service_implementation():
    """Test that a proper concrete implementation works."""

    class ConcreteService(BaseService):
        def execute(self, data):
            return {"result": data}

    service = ConcreteService()
    result = service.execute("test")
    assert result == {"result": "test"}


def test_service_error_inheritance():
    """Test that ServiceError is properly inherited from TemplateError."""
    from py_template import TemplateError

    error = ServiceError("Test error")
    assert isinstance(error, TemplateError)
    assert isinstance(error, Exception)
    assert str(error) == "Test error"


def test_service_error_raising():
    """Test raising ServiceError in a service."""

    class FailingService(BaseService):
        def execute(self, data):
            raise ServiceError("Service failed")

    service = FailingService()
    with pytest.raises(ServiceError, match="Service failed"):
        service.execute("test")
