# Template Usage Guide

This guide explains how to use py_template to start your own Python project.

## Quick Start Checklist

- [ ] Clone/fork this repository
- [ ] Rename the package directory
- [ ] Update pyproject.toml
- [ ] Update all imports
- [ ] Customize or remove example modules
- [ ] Update documentation
- [ ] Initialize your git repository
- [ ] Start developing!

## Detailed Steps

### Step 1: Get the Template

**Option A: GitHub Template (Recommended)**

1. Click "Use this template" on GitHub
2. Create your new repository
3. Clone your repository

**Option B: Manual Clone**

```bash
git clone <this-repo-url> my-awesome-project
cd my-awesome-project
rm -rf .git  # Remove template's git history
git init     # Start fresh
```

### Step 2: Rename the Package

**Manual Renaming**:

1. Rename directory:

   ```bash
   mv src/py_template src/my_package
   ```

2. Update pyproject.toml:

   ```toml
   name = "my_package"

   [tool.hatch.version]
   path = "src/my_package/__version__.py"

   [tool.hatch.build.targets.wheel]
   packages = ["src/my_package"]

   [project.scripts]
   my_cli = "my_package.cli.commands:main"
   ```

3. Update all imports (use find & replace):

   ```bash
   # Find all occurrences
   grep -r "py_template" src/ tests/

   # Replace in all Python files
   find src tests -name "*.py" -type f -exec sed -i '' 's/py_template/my_package/g' {} +
   ```

4. Update Docker files:
   - Dockerfile: Update paths and usernames
   - docker-compose.yml: Update service names and commands

### Step 3: Customize Project Information

Update `pyproject.toml`:

```toml
[project]
name = "my-awesome-project"
description = "Your project description here"
authors = [{ name = "Your Name", email = "your.email@example.com" }]
keywords = ["your", "keywords", "here"]

dependencies = [
    "pydantic>=2.11.5",
    "click>=8.1.0",
    # Add your dependencies here
]
```

Update `src/my_package/__version__.py`:

```python
__version__ = "0.1.0"
```

Update `LICENSE`:

- Replace with your chosen license
- Update copyright holder

### Step 4: Decide on Example Modules

The template includes an example service module:

- `src/py_template/services/`

**Option A: Keep and Extend**

If the service pattern fits your domain, keep it and add your implementations:

```python
from py_template.services import BaseService

class MyService(BaseService):
    def execute(self, data):
        # Your service logic
        return result
```

**Option B: Replace**

Rename it to match your domain (e.g., `handlers/`, `controllers/`, `models/`, etc.)

**Option C: Remove**

If you don't need it:

```bash
rm -rf src/my_package/services
# Update src/my_package/__init__.py to remove BaseService export
```

### Step 5: Customize the CLI

Edit `src/my_package/cli/commands.py`:

```python
@click.group()
@click.version_option(version=__version__, prog_name="my-cli")
def main():
    """My Awesome CLI Tool."""

# Add your commands
@main.command()
def my_command():
    """My custom command."""
    click.echo("Hello from my command!")
```

### Step 6: Install and Test

```bash
# Remove old virtual environment
rm -rf .venv

# Install with new configuration
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install

# Test your CLI
uv run my-cli --version
uv run my-cli --help

# Run tests
uv run pytest
```

### Step 7: Update Documentation

1. **README.md**: Update with your project's purpose and usage
2. **docs/api.md**: Document your API
3. **docs/development.md**: Update development instructions
4. **Remove this file**: Delete `docs/TEMPLATE_USAGE.md` once setup is complete

### Step 8: Set Up Version Control

```bash
git add .
git commit -m "Initial commit from py_template"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Step 9: Configure GitHub (if using)

1. **Secrets** (for GitHub Actions):
   - No secrets needed for basic CI
   - Add `CODECOV_TOKEN` for coverage reporting (optional)

2. **Branch Protection** (optional):
   - Protect `main` branch
   - Require PR reviews
   - Require status checks to pass

3. **Enable Workflows**:
   - Go to Actions tab
   - Enable workflows if needed

## Advanced Customization

### Adding Dependencies

```bash
# Add runtime dependency
uv add requests

# Add development dependency
uv add --dev mypy

# Update lock file
uv lock
```

### Customizing Code Quality Tools

Edit `pyproject.toml`:

```toml
[tool.ruff]
line-length = 120  # Change line length

[tool.ruff.lint]
ignore = ["E501"]  # Ignore specific rules
```

Edit `.pre-commit-config.yaml` to add/remove hooks.

### Adding More GitHub Workflows

Create new files in `.github/workflows/`:

```yaml
name: My Custom Workflow
on:
  push:
    branches: [main]
jobs:
  custom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Add your steps
```

### Database Support

If you need database support:

1. Add dependencies:

   ```bash
   uv add sqlalchemy alembic  # or asyncpg, psycopg2, etc.
   ```

2. Create `src/my_package/db/` module
3. Add database configuration
4. Update Docker Compose to include database service

### API Server

To convert this into a web API:

1. Add FastAPI:

   ```bash
   uv add fastapi uvicorn
   ```

2. Create `src/my_package/api/` module
3. Update Dockerfile to expose ports
4. Update CLI to include `serve` command

## Troubleshooting

### Import Errors After Renaming

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstall
rm -rf .venv
uv sync --extra dev
```

### Pre-commit Hooks Failing

```bash
# Run hooks manually to see details
uv run pre-commit run --all-files

# Update hooks
uv run pre-commit autoupdate
```

### Docker Build Failures

```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker build --no-cache -t my-project:dev .
```

## Example: Creating a Simple Web API Project

Here's a complete example of converting this template into a FastAPI project:

```bash
# Step 1: Clone and rename
git clone <template-repo> my-api
cd my-api
mv src/py_template src/my_api

# Step 2: Add FastAPI
uv add fastapi uvicorn

# Step 3: Update imports
find src tests -name "*.py" -exec sed -i '' 's/py_template/my_api/g' {} +

# Step 4: Update pyproject.toml
# ... edit file ...

# Step 5: Create API module
mkdir src/my_api/api
cat > src/my_api/api/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
EOF

# Step 6: Update CLI to add serve command
# ... edit src/my_api/cli/commands.py ...

# Step 7: Test
uv sync --extra dev
uv run uvicorn my_api.api.main:app --reload
```

## Getting Help

- Check [Development Guide](development.md) for workflow details
- Review [Project Standards](project-standards.md) for code conventions
- Open an issue on the template repository for template-specific questions

## Next Steps

Once setup is complete:

1. Write your first feature
2. Add tests for your feature
3. Update documentation
4. Create your first release

Happy coding!
