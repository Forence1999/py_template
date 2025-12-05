# Multi-stage Dockerfile for py_template
# This provides a containerized development and testing environment

# ============================================================================
# Stage 1: Builder - Install dependencies
# ============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./
COPY src/py_template/__version__.py ./src/py_template/__version__.py

# Create virtual environment and install dependencies
# Use --frozen to ensure reproducible builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ============================================================================
# Stage 2: Development - For development and testing
# ============================================================================
FROM python:3.12-slim AS development

WORKDIR /app

# Copy uv from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./
COPY src/py_template/__version__.py ./src/py_template/__version__.py

# Install all dependencies including dev
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --extra dev

# Copy source code
COPY . .

# Set Python path
ENV PYTHONPATH=/app/src
ENV PATH="/app/.venv/bin:$PATH"

# Default command: run tests
CMD ["pytest", "-v"]

# ============================================================================
# Stage 3: Runtime - Minimal runtime for using the library
# ============================================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 pytemplate && \
    chown -R pytemplate:pytemplate /app

USER pytemplate

# Default command: show info
CMD ["py_template", "info"]

# ============================================================================
# Stage 4: Testing - For CI/CD
# ============================================================================
FROM development AS testing

# Copy test files
COPY tests/ ./tests/

# Run tests with coverage
CMD ["pytest", "--cov=src", "--cov-report=xml", "--cov-report=term"]

# ============================================================================
# Usage Examples:
# ============================================================================
#
# Build for development:
#   docker build --target development -t py_template:dev .
#
# Build for runtime:
#   docker build --target runtime -t py_template:latest .
#
# Build for testing:
#   docker build --target testing -t py_template:test .
#
# Run development container:
#   docker run -it --rm -v $(pwd):/app py_template:dev bash
#
# Run tests:
#   docker run --rm py_template:test
#
# Run CLI:
#   docker run --rm py_template:latest py_template info
#
# Interactive Python with py_template:
#   docker run -it --rm py_template:latest python
