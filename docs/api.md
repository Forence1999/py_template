# API Documentation

## Core Modules

### Exceptions

py_template provides a hierarchy of custom exceptions:

#### `TemplateError`

Base exception for all py_template errors.

```python
from py_template import TemplateError

try:
    # Your code
    pass
except TemplateError as e:
    print(f"Template error: {e}")
```

#### `ValidationError`

Raised when data validation fails.

```python
from py_template import ValidationError

try:
    # Validation code
    pass
except ValidationError as e:
    print(f"Validation failed: {e}")
```

#### `ServiceError`

Raised when service execution fails.

```python
from py_template import ServiceError

try:
    # Service execution code
    pass
except ServiceError as e:
    print(f"Service failed: {e}")
```

### Models

#### `BaseModel`

Pydantic-based base model for all py_template data structures.

```python
from py_template import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# Create an instance
user = User(name="Alice", age=30, email="alice@example.com")

# Validation happens automatically
try:
    invalid_user = User(name="Bob", age="not a number", email="bob@example.com")
except ValidationError as e:
    print(e)
```

**Configuration:**

- `validate_assignment=True`: Validates data on assignment
- `arbitrary_types_allowed=False`: Only allows standard types

## Base Classes

### Services

#### `BaseService`

Abstract base class for all services. Services encapsulate business logic, external API interactions, or data processing operations.

```python
from py_template import BaseService, ServiceError
from typing import Any

class MyService(BaseService):
    def execute(self, data: Any) -> Any:
        """Execute the service operation."""
        # Your service logic here
        if not data:
            raise ServiceError("Data cannot be empty")
        return {"processed": data}

# Usage
service = MyService()
result = service.execute({"input": "value"})
print(result)  # {"processed": {"input": "value"}}
```

**Real-world Example:**

```python
from py_template import BaseService, ServiceError
import requests

class UserService(BaseService):
    """Service for managing user operations."""

    def __init__(self, api_url: str):
        self.api_url = api_url

    def execute(self, user_id: int) -> dict:
        """Fetch user data from API."""
        try:
            response = requests.get(f"{self.api_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ServiceError(f"Failed to fetch user {user_id}: {e}")

# Usage
service = UserService(api_url="https://api.example.com")
user_data = service.execute(123)
```

**Method Signature:**

- `execute(data: Any) -> Any`: Abstract method that must be implemented by subclasses
- Parameters: Flexible - can accept any type of data
- Returns: Any type - depends on the service implementation
- Raises: `ServiceError` when the operation fails

## Utility Functions

### `ensure_list`

Ensures a value is a list.

```python
from py_template.utils.helpers import ensure_list

# Single value becomes a list
result = ensure_list("value")  # ["value"]

# List stays as list
result = ensure_list([1, 2, 3])  # [1, 2, 3]
```

## CLI Commands

### `info`

Display py_template version and information.

```bash
py_template info
# Output:
# py_template v0.1.0
# A powerful data processing toolkit
```

### `--version`

Show version number.

```bash
py_template --version
# Output: py_template, version 0.1.0
```

## Complete Example

Here's a complete example showing how to use py_template:

```python
from py_template import BaseModel, BaseService, ServiceError, ValidationError

# Define your data model
class DataRecord(BaseModel):
    id: int
    name: str
    value: float

# Create a custom service for data processing
class DataProcessingService(BaseService):
    """Service that processes and validates data records."""

    def execute(self, data: dict) -> DataRecord:
        """Process raw data and return a validated DataRecord."""
        try:
            # Clean the data
            cleaned = {k: v for k, v in data.items() if v is not None}

            # Normalize values
            if 'value' in cleaned:
                cleaned['value'] = float(cleaned['value']) / 100.0

            # Validate and create model
            record = DataRecord(**cleaned)
            return record

        except ValidationError as e:
            raise ServiceError(f"Data validation failed: {e}")
        except Exception as e:
            raise ServiceError(f"Processing failed: {e}")

# Create another service for business logic
class DataStorageService(BaseService):
    """Service that stores data records."""

    def __init__(self):
        self.storage = []

    def execute(self, record: DataRecord) -> dict:
        """Store a data record and return confirmation."""
        self.storage.append(record)
        return {
            "success": True,
            "record_id": record.id,
            "total_records": len(self.storage)
        }

# Use them together
try:
    # Raw data
    raw_data = {"id": 1, "name": "Test", "value": 50.0, "extra": None}

    # Process the data
    processor = DataProcessingService()
    record = processor.execute(raw_data)
    print(f"Processed record: {record}")

    # Store the data
    storage = DataStorageService()
    result = storage.execute(record)
    print(f"Storage result: {result}")

except ServiceError as e:
    print(f"Service error: {e}")
except TemplateError as e:
    print(f"Template error: {e}")
```

**Output:**

```
Processed record: id=1 name='Test' value=0.5
Storage result: {'success': True, 'record_id': 1, 'total_records': 1}
```

## Best Practices

### Error Handling

Always catch specific exceptions and handle them appropriately:

```python
from py_template import ServiceError, ValidationError, TemplateError

try:
    service.execute(data)
except ValidationError as e:
    # Handle validation errors
    logger.error(f"Invalid data: {e}")
except ServiceError as e:
    # Handle service errors
    logger.error(f"Service failed: {e}")
except TemplateError as e:
    # Catch-all for other template errors
    logger.error(f"Unexpected error: {e}")
```

### Service Design

- Keep services focused on a single responsibility
- Use dependency injection for external dependencies
- Raise `ServiceError` for recoverable errors
- Document the expected input and output types

```python
from py_template import BaseService, ServiceError

class EmailService(BaseService):
    """Service for sending emails.

    Example:
        >>> service = EmailService(smtp_host="smtp.example.com")
        >>> result = service.execute({
        ...     "to": "user@example.com",
        ...     "subject": "Hello",
        ...     "body": "Welcome!"
        ... })
    """

    def __init__(self, smtp_host: str, smtp_port: int = 587):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def execute(self, email_data: dict) -> dict:
        """Send an email.

        Args:
            email_data: Dict with 'to', 'subject', and 'body' keys

        Returns:
            Dict with 'success' and 'message_id' keys

        Raises:
            ServiceError: If email sending fails
        """
        # Implementation here
        pass
```
