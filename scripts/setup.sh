#!/bin/bash

# py_template Setup Script

set -e

echo "Setting up py_template development environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
	echo "Installing uv..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
	echo "Please restart your shell and run this script again."
	exit 0
fi

# Install dependencies
echo "Installing dependencies..."
uv sync --extra dev

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "Setup complete! You can now start developing."
echo "Run 'uv run pytest' to verify the installation."
