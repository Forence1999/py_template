# Development Guide

## Setup

1. Install uv
2. Clone the repository
3. Run `bash scripts/setup.sh`

## Code Standards

- Follow PEP 8 (enforced by Ruff)
- Maximum line length: 100 characters
- Use type hints where appropriate
- Write docstrings for all public APIs

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_models.py
```

## Code Quality

```bash
# Format code
uv run ruff format

# Check code
uv run ruff check --fix

# Run pre-commit on all files
uv run pre-commit run --all-files
```

## Project Structure

The project follows the modern Python src layout:

```
py_template/
├── src/py_template/        # Source code
│   ├── cli/                # Command-line interface
│   ├── core/               # Core functionality
│   ├── services/           # Service modules
│   └── utils/              # Utility functions
├── tests/                  # Test files
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                   # Documentation
└── scripts/                # Development scripts
```

## Adding New Modules

### Creating a Service

```python
from py_template.services import BaseService

class MyService(BaseService):
    def execute(self, data):
        # Your service logic here
        # Example: API call, business logic, data processing
        result = self._process_data(data)
        return result

    def _process_data(self, data):
        # Helper method
        return {"processed": data}
```

Example usage:

```python
from py_template import ServiceError

class UserService(BaseService):
    def execute(self, user_id: int) -> dict:
        if user_id < 0:
            raise ServiceError("Invalid user ID")
        return {"user_id": user_id, "name": "John Doe"}

# Use the service
service = UserService()
result = service.execute(123)
print(result)  # {"user_id": 123, "name": "John Doe"}
```

## Dependency Management

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade

# View dependency tree
uv tree
```

## Git Workflow

```bash
# Create a feature branch
git checkout -b feature/new-feature

# Make changes and commit (pre-commit will run automatically)
git add .
git commit -m "feat: add new feature"

# Push changes
git push origin feature/new-feature
```

## Best Practices

1. **Write tests first**: Follow TDD when possible
2. **Keep it simple**: Avoid over-engineering
3. **Document your code**: Use clear docstrings
4. **Use type hints**: They help catch bugs early
5. **Run tests frequently**: Ensure nothing breaks
