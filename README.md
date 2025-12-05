# py_template

A minimal Python project template with modern tooling and best practices.

## Features

- 🏗️ Modern Python packaging with `pyproject.toml` and `uv`
- 🔍 Code quality tools: Ruff for linting and formatting
- ✅ Pre-commit hooks for automated code quality checks
- 🧪 Comprehensive test framework with pytest
- 🐳 Docker support for development and deployment
- 🚀 GitHub Actions CI/CD workflows
- 📁 Well-structured project layout with `src/` pattern
- 🖥️ Example CLI application using Click
- 📚 Comprehensive documentation

## Quick Start

### Using This Template

**Option 1: Use as GitHub Template**
1. Click "Use this template" button on GitHub
2. Clone your new repository
3. Follow customization steps below

**Option 2: Manual Setup**
```bash
# Clone this repository
git clone <this-repo> my-project
cd my-project

# Rename the package directory
mv src/py_template src/my_package

# Update pyproject.toml with your project info
# Update imports in all Python files
# See docs/TEMPLATE_USAGE.md for detailed instructions
```

### Installation (Development)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install
```

## Usage

### Example CLI

This template includes a sample CLI application:

```bash
# Show version and info
uv run py_template --version
uv run py_template info

# Hello world example
uv run py_template hello
uv run py_template hello --name "Developer"
```

### Example Code

```python
from py_template import BaseModel, __version__

print(f"py_template v{__version__}")

# Example: Using the base model
class User(BaseModel):
    name: str
    age: int

user = User(name="Alice", age=30)
print(user)
```

## Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Format code
uv run ruff format

# Lint code
uv run ruff check --fix
```

## Project Structure

```
.
├── src/py_template/       # Main package code
│   ├── cli/              # Command-line interface
│   ├── core/             # Core models and exceptions
│   ├── services/         # Service modules (example)
│   └── utils/            # Utility functions
├── tests/                # Test files
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── docs/                 # Documentation
├── .github/workflows/    # CI/CD workflows
└── pyproject.toml        # Project configuration
```

## Documentation

- [Template Usage Guide](docs/TEMPLATE_USAGE.md) - **Start here!** How to use this template
- [Development Guide](docs/development.md) - Development workflow
- [API Documentation](docs/api.md) - API reference
- [Docker Guide](docs/docker.md) - Docker usage
- [Deployment Guide](docs/deployment.md) - Deployment strategies
- [Release Process](docs/release.md) - How to create releases

## Customization

### Replace Package Name

This template uses `py_template` as the package name. To customize:

1. Rename `src/py_template/` to `src/your_package_name/`
2. Update `pyproject.toml` with your project details
3. Update all imports from `py_template` to `your_package_name`
4. Update Docker and CI/CD configurations

See [Template Usage Guide](docs/TEMPLATE_USAGE.md) for detailed steps.

### Adapt Example Modules

The template includes example service modules:
- **Keep them** if they fit your use case
- **Replace them** with your own modules
- **Remove them** if you don't need them

## What's Included

### Core Tools

- **Package Manager**: uv (fast, modern Python package manager)
- **Linter/Formatter**: Ruff (extremely fast Python linter)
- **Test Framework**: pytest with coverage support
- **CLI Framework**: Click (for building command-line interfaces)
- **Data Validation**: Pydantic (for data modeling)

### Quality Assurance

- Pre-commit hooks for automatic code quality checks
- GitHub Actions workflows for CI/CD
- Code coverage reporting
- Security scanning (Bandit + Safety)

### Docker Support

- Multi-stage Dockerfile for development, testing, and production
- Docker Compose setup with multiple services
- Optimized layer caching for fast builds

## Contributing

Contributions are welcome! See [Development Guide](docs/development.md) for details.

## License

MIT License (see LICENSE file)

---

**Made with py_template** - A Python project template
