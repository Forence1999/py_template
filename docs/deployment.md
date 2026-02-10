# Deployment Guide

## Overview

py_template is a Python library that can be deployed in various ways depending on your use case. This guide covers common deployment scenarios.

## Package Distribution

### Building the Package

```bash
# Install build tools
uv add --dev build

# Build the distribution packages
uv run python -m build

# This creates:
# - dist/py_template-0.1.0.tar.gz (source distribution)
# - dist/py_template-0.1.0-py3-none-any.whl (wheel)
```

### Local Installation

```bash
# Install from local directory
pip install /path/to/py_template

# Install in editable mode (for development)
pip install -e /path/to/py_template
```

### Private Package Repository

For proprietary software, you can use a private package repository:

#### Using PyPI Server (Self-hosted)

```bash
# Install pypiserver
pip install pypiserver

# Start server
pypi-server -p 8080 /path/to/packages

# Upload package
twine upload --repository-url http://localhost:8080 dist/*

# Install from private server
pip install --index-url http://localhost:8080/simple/ py_template
```

#### Using Artifactory or Nexus

Configure your `.pypirc`:

```ini
[distutils]
index-servers =
    private-repo

[private-repo]
repository: https://your-artifactory.com/repository/pypi/
username: your-username
password: your-password
```

Upload:

```bash
twine upload -r private-repo dist/*
```

## Git-based Deployment

### Direct Installation from Git

```bash
# Install from main branch
pip install git+https://github.com/your-org/py_template.git

# Install from specific tag
pip install git+https://github.com/your-org/py_template.git@v0.1.0

# Install from specific branch
pip install git+https://github.com/your-org/py_template.git@dev
```

### Using requirements.txt

```txt
# requirements.txt
py_template @ git+https://github.com/your-org/py_template.git@v0.1.0
```

### Using pyproject.toml

```toml
[project.dependencies]
py_template = { git = "https://github.com/your-org/py_template.git", tag = "v0.1.0" }
```

## Environment Setup

### Production Environment

```bash
# Install only production dependencies
uv sync --no-dev

# Or with pip
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Docker Deployment (Optional)

While py_template is a library, you might want to containerize applications that use it:

### Dockerfile Example

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --no-dev --frozen

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app/src

CMD ["python", "-m", "your_app"]
```

## CI/CD Integration

### GitHub Actions

The project includes pre-configured workflows:

- **CI** ([.github/workflows/ci.yml](.github/workflows/ci.yml)) - Runs tests and linting
- **Security** ([.github/workflows/security.yml](.github/workflows/security.yml)) - Security scanning
- **Code Quality** ([.github/workflows/code-quality.yml](.github/workflows/code-quality.yml)) - Code quality checks

### Release Process

1. Update version in [src/py_template/**version**.py](src/py_template/__version__.py)
2. Update [CHANGELOG.md](CHANGELOG.md)
3. Create a git tag:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```
4. Build and distribute the package

## Version Management

### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

### Version Bumping

```bash
# Manually update version in src/py_template/__version__.py
# Then commit and tag
git commit -am "Bump version to 0.2.0"
git tag -a v0.2.0 -m "Release version 0.2.0"
git push && git push --tags
```

## Monitoring and Maintenance

### Health Checks

For applications using py_template:

```python
from py_template import __version__

def health_check():
    """Verify py_template is installed and working."""
    return {
        "status": "healthy",
        "py_template_version": __version__
    }
```

### Dependency Updates

```bash
# Update dependencies
uv sync --upgrade

# Check for security vulnerabilities
uv run safety check

# Review and commit uv.lock
git add uv.lock
git commit -m "Update dependencies"
```

## Rollback Procedures

### Git-based Rollback

```bash
# Revert to previous version
pip install git+https://github.com/your-org/py_template.git@v0.0.9
```

### Package Rollback

```bash
# Install specific version
pip install py_template==0.0.9
```

## Security Considerations

1. **Private Repository**: Keep your repository private since this is proprietary software
2. **Access Control**: Limit access to the package repository
3. **Dependency Scanning**: Regularly scan dependencies for vulnerabilities
4. **Code Signing**: Consider signing your packages
5. **Secret Management**: Never commit API keys or credentials

## Support and Troubleshooting

### Common Issues

**Import Errors**

```bash
# Ensure PYTHONPATH is set correctly
export PYTHONPATH=/path/to/installation/src
```

**Dependency Conflicts**

```bash
# Use virtual environment
uv venv
source .venv/bin/activate
uv sync
```

### Getting Help

- Check [README.md](README.md) for basic usage
- Review [development.md](development.md) for development setup
- See [api.md](api.md) for API documentation

## Backup and Recovery

### Backup Strategy

1. **Source Code**: Keep in version control (Git)
2. **Dependencies**: Lock files (uv.lock) ensure reproducibility
3. **Configuration**: Store `.env.example` in version control

### Recovery

```bash
# Clone repository
git clone https://github.com/your-org/py_template.git
cd py_template

# Restore dependencies
uv sync

# Verify installation
uv run py_template info
```
