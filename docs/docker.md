# Docker Guide

This guide covers using Docker with py_template for development, testing, and deployment.

## Overview

py_template provides Docker support for:

- **Development** - Consistent development environment
- **Testing** - Isolated test execution
- **Runtime** - Minimal production-ready image
- **CI/CD** - Reproducible builds

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Run tests
docker-compose up test

# Start development environment
docker-compose run --rm dev bash

# Run linting
docker-compose up lint

# Interactive Python shell
docker-compose run --rm shell
```

### Using Docker CLI

```bash
# Build development image
docker build --target development -t py_template:dev .

# Run tests
docker run --rm py_template:dev pytest

# Interactive development
docker run -it --rm -v $(pwd)/src:/app/src py_template:dev bash
```

## Docker Images

### 1. Development Image

**Target:** `development`

**Purpose:** Full development environment with all dependencies

**Includes:**
- All development dependencies (pytest, ruff, etc.)
- Testing tools
- Development utilities

**Usage:**
```bash
# Build
docker build --target development -t py_template:dev .

# Run interactive shell
docker run -it --rm \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/tests:/app/tests \
  py_template:dev bash

# Inside container
pytest
ruff check src
py_template info
```

### 2. Runtime Image

**Target:** `runtime`

**Purpose:** Minimal image for using py_template library

**Includes:**
- Python runtime
- py_template and its dependencies
- No development tools

**Usage:**
```bash
# Build
docker build --target runtime -t py_template:latest .

# Run CLI
docker run --rm py_template:latest py_template info

# Interactive Python
docker run -it --rm py_template:latest python
```

### 3. Testing Image

**Target:** `testing`

**Purpose:** Run tests with coverage

**Includes:**
- All test dependencies
- Test files
- Coverage tools

**Usage:**
```bash
# Build
docker build --target testing -t py_template:test .

# Run tests
docker run --rm py_template:test

# Run with coverage report
docker run --rm \
  -v $(pwd)/coverage:/app/coverage \
  py_template:test pytest --cov=src --cov-report=html
```

## Docker Compose Services

### Service: `dev`

Development environment with interactive shell.

```bash
# Start
docker-compose run --rm dev bash

# Run commands inside container
pytest
ruff check src
python -m py_template.cli.commands
```

### Service: `test`

Run test suite with coverage.

```bash
# Run all tests
docker-compose up test

# Run specific test
docker-compose run --rm test pytest tests/unit/test_models.py

# With custom pytest args
PYTEST_ARGS="-v -k test_specific" docker-compose up test
```

### Service: `lint`

Code quality checks.

```bash
# Run linting
docker-compose up lint

# Just check, don't fix
docker-compose run --rm lint ruff check src tests
```

### Service: `runtime`

Runtime environment.

```bash
# Show info
docker-compose up runtime

# Run CLI command
docker-compose run --rm runtime py_template --version
```

### Service: `shell`

Interactive Python shell with py_template imported.

```bash
# Start Python shell
docker-compose run --rm shell

# Inside Python shell:
>>> from py_template import BaseModel, __version__
>>> print(__version__)
```

## Development Workflow

### 1. Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd py_template

# Build images
docker-compose build
```

### 2. Daily Development

```bash
# Start development environment
docker-compose run --rm dev bash

# Inside container:
# - Edit code (files are mounted from host)
# - Run tests: pytest
# - Check code: ruff check src
# - Format code: ruff format src
```

### 3. Running Tests

```bash
# Run all tests
docker-compose up test

# Run with watch mode (requires pytest-watch)
docker-compose run --rm dev ptw

# Run specific test file
docker-compose run --rm test pytest tests/unit/test_models.py -v
```

### 4. Code Quality

```bash
# Run all quality checks
docker-compose up lint

# Auto-fix issues
docker-compose run --rm dev bash -c "ruff check --fix src tests && ruff format src tests"
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/docker.yml
name: Docker Build

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build test image
        run: docker build --target testing -t py_template:test .

      - name: Run tests
        run: docker run --rm py_template:test

      - name: Build runtime image
        run: docker build --target runtime -t py_template:latest .
```

### Local CI Simulation

```bash
# Run same checks as CI
docker-compose up --abort-on-container-exit lint test
```

## Advanced Usage

### Multi-Architecture Builds

```bash
# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --target runtime \
  -t py_template:latest .
```

### Build with Custom Arguments

```bash
# Build with specific Python version
docker build \
  --build-arg PYTHON_VERSION=3.12 \
  --target runtime \
  -t py_template:py312 .
```

### Volume Mounts for Development

```bash
# Mount source code for live editing
docker run -it --rm \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/tests:/app/tests \
  -e PYTHONPATH=/app/src \
  py_template:dev bash
```

### Running with Custom Environment

```bash
# Use .env file
docker-compose --env-file .env.custom up dev

# Override environment variables
docker-compose run --rm \
  -e DEBUG=true \
  -e LOG_LEVEL=DEBUG \
  dev pytest -v
```

## Image Optimization

### Size Comparison

```bash
# Check image sizes
docker images py_template

# Expected sizes:
# development: ~500MB (includes all dev tools)
# runtime: ~200MB (minimal production image)
# testing: ~450MB (includes test dependencies)
```

### Build Cache

```bash
# Use cache for faster builds
docker build --target development -t py_template:dev .

# Force rebuild without cache
docker build --no-cache --target development -t py_template:dev .

# Clean build cache
docker builder prune
```

### Layer Optimization

The Dockerfile uses multi-stage builds to:
1. Separate build dependencies from runtime
2. Cache dependency installations
3. Minimize final image size

## Troubleshooting

### Problem: Slow builds

**Solution:** Use BuildKit and cache mounts

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with cache
docker build --target development -t py_template:dev .
```

### Problem: Permission issues

**Solution:** Use non-root user (already configured in runtime image)

```bash
# Check user in container
docker run --rm py_template:latest id
# Should show: uid=1000(py_template) gid=1000(py_template)
```

### Problem: Import errors

**Solution:** Ensure PYTHONPATH is set

```bash
# Check PYTHONPATH
docker run --rm py_template:latest env | grep PYTHONPATH
# Should show: PYTHONPATH=/app/src

# Or set it manually
docker run --rm -e PYTHONPATH=/app/src py_template:latest python
```

### Problem: Tests fail in Docker but pass locally

**Solution:** Check dependencies and environment

```bash
# Compare dependency versions
docker run --rm py_template:dev pip list > docker-deps.txt
pip list > local-deps.txt
diff docker-deps.txt local-deps.txt

# Check environment variables
docker run --rm py_template:dev env
```

## Best Practices

### 1. Use Multi-Stage Builds

- Keep development image separate from runtime
- Share base layers when possible
- Minimize final image size

### 2. Leverage Build Cache

```dockerfile
# Copy only dependency files first
COPY pyproject.toml uv.lock ./
RUN uv sync

# Then copy source code
COPY src/ ./src/
```

### 3. Use .dockerignore

Exclude unnecessary files to speed up builds:
- `.git/`
- `__pycache__/`
- `.venv/`
- IDE files

### 4. Pin Versions

```dockerfile
# Good - specific version
FROM python:3.12-slim

# Avoid - latest can change
FROM python:latest
```

### 5. Run as Non-Root

The runtime image uses a non-root user `py_template` for security.

### 6. Health Checks (Optional)

For applications using py_template:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "from py_template import __version__; print(__version__)" || exit 1
```

## Production Deployment

### Container Registry

```bash
# Tag for registry
docker tag py_template:latest registry.example.com/py_template:0.1.0

# Push to registry
docker push registry.example.com/py_template:0.1.0
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: py_template-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: registry.example.com/py_template:0.1.0
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

## Maintenance

### Regular Updates

```bash
# Update base image
docker pull python:3.12-slim

# Rebuild images
docker-compose build --no-cache

# Test updated images
docker-compose up test
```

### Cleanup

```bash
# Remove unused images
docker image prune -a

# Remove all py_template images
docker images | grep py_template | awk '{print $3}' | xargs docker rmi

# Clean everything
docker-compose down -v
docker system prune -af
```

## Resources

- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [BuildKit](https://docs.docker.com/build/buildkit/)
