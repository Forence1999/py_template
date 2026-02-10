# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Template Features

This is a Python project template that includes:

- Modern Python packaging with pyproject.toml and uv
- Code quality tools (Ruff, pre-commit)
- Comprehensive test framework with pytest
- Docker support with multi-stage builds
- GitHub Actions CI/CD workflows
- Example CLI application using Click
- Well-structured project layout with src/ pattern
- Complete documentation

## How to Use

When you start using this template for your project:

1. Keep this CHANGELOG.md file
2. Remove the "Template Features" section above
3. Start documenting your changes from version 0.1.0
4. Follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format

---

## Version History

## [1.0.1] - 2026-02-10

### Changed

- **Code Formatting Standardization**: Unified indentation standards across all file types
  - Python: 4 spaces (PEP 8 standard)
  - JSON/YAML: 2 spaces (industry standard)
  - Markdown/HTML/XML: 2 spaces (W3C/Google style guide)
  - Shell scripts: 2 spaces (Google Shell Style Guide)
  - JavaScript/TypeScript: 2 spaces
- Updated `.editorconfig` with comprehensive file type rules and Chinese comments
- Updated `.prettierrc` with per-file-type overrides for consistent formatting
- Updated `.vscode/settings.json` with explicit tab sizes for all language modes
- Updated `pyproject.toml` ruff configuration with `line-ending = "lf"` setting
- Applied formatting to all project files using Prettier and Ruff
- Added "Code Style" section to README documenting indentation conventions

## [1.0.0] - 2026-02-10

### Added

- Initial stable release of py_template
- Modern Python packaging with `pyproject.toml` and `uv`
- Code quality tools: Ruff for linting and formatting
- Pre-commit hooks for automated code quality checks
- Comprehensive test framework with pytest and coverage
- Docker support with multi-stage builds
- GitHub Actions CI/CD workflows (CI, code quality, security, release)
- Example CLI application using Click
- Well-structured project layout with `src/` pattern
- Complete documentation (development, deployment, API, Docker, release guides)
- Security scanning with Bandit and Safety
