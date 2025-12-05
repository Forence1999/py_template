"""pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {"key": "value", "number": 42}
