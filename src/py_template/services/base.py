"""Base service class for the template.

This module provides an abstract base class for implementing services.
Services typically encapsulate business logic, external API interactions,
or data access operations.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Abstract base class for services.

    This class defines the interface that all service implementations
    should follow. Extend this class to create concrete service implementations.

    Example:
        >>> class UserService(BaseService):
        ...     def execute(self, data: dict) -> dict:
        ...         # Implementation here
        ...         return {"user_id": data["id"], "name": "John"}
    """

    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the service operation.

        Args:
            data: Input data for the service operation.

        Returns:
            The result of the service operation.

        Raises:
            ServiceError: If the service operation fails.
        """
