# Release Process

This document describes the release process for py_template.

## Overview

py_template uses automated GitHub Actions workflows for releases. The release process includes:

1. Building distribution packages (source and wheel)
2. Creating GitHub releases with changelog
3. Optional: Publishing to PyPI or private repository
4. Notification and summary

## Prerequisites

Before creating a release:

1. ✅ All tests pass on `main` branch
2. ✅ Code quality checks pass
3. ✅ CHANGELOG.md is updated with release notes
4. ✅ Version number is bumped in `src/py_template/__version__.py`
5. ✅ All changes are committed and pushed

## Release Methods

### Method 1: Tag-based Release (Recommended)

Create and push a version tag to trigger automatic release:

```bash
# 1. Update version
vim src/py_template/__version__.py
# Change __version__ = "0.2.0"

# 2. Update CHANGELOG.md
vim CHANGELOG.md
# Add new version section with changes

# 3. Commit changes
git add src/py_template/__version__.py CHANGELOG.md
git commit -m "Bump version to 0.2.0"

# 4. Create and push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main
git push origin v0.2.0
```

The workflow will automatically:
- Build distribution packages
- Create GitHub release with changelog
- Upload artifacts (`.tar.gz` and `.whl` files)

### Method 2: Manual Workflow Dispatch

Trigger release manually from GitHub Actions UI:

1. Go to **Actions** → **Release** workflow
2. Click **Run workflow**
3. Select branch: `main`
4. Enter version: `0.2.0` (without 'v' prefix)
5. Click **Run workflow**

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

Examples:
- 0.1.0 → 0.2.0 (new features, backward compatible)
- 0.2.0 → 0.2.1 (bug fixes, backward compatible)
- 0.2.1 → 1.0.0 (major changes, potentially breaking)
```

**Pre-release versions:**
- `0.1.0-alpha.1` - Alpha release
- `0.1.0-beta.1` - Beta release
- `0.1.0-rc.1` - Release candidate

## Release Workflow Details

### Jobs

1. **build** - Build distribution packages
   - Installs dependencies
   - Builds source distribution (`.tar.gz`)
   - Builds wheel distribution (`.whl`)
   - Validates packages with `twine check`
   - Uploads artifacts

2. **publish-github** - Create GitHub release
   - Downloads build artifacts
   - Extracts version from tag
   - Generates changelog from CHANGELOG.md
   - Creates GitHub release with artifacts
   - Marks release as published

3. **publish-pypi** (Optional, commented out)
   - Publishes to PyPI
   - Requires `PYPI_API_TOKEN` secret

4. **publish-private** (Optional, commented out)
   - Publishes to private repository
   - Requires repository URL and credentials

5. **notify** - Send notification
   - Generates release summary
   - Updates GitHub Step Summary

## Publishing to PyPI (Optional)

If you want to publish to PyPI, uncomment the `publish-pypi` job in `.github/workflows/release.yml`:

### Setup

1. Create PyPI API token:
   - Go to https://pypi.org/manage/account/token/
   - Create new token with scope: "Entire account" or specific to "py_template"
   - Copy the token (starts with `pypi-`)

2. Add token to GitHub Secrets:
   - Go to repository **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token
   - Click **Add secret**

3. Uncomment the `publish-pypi` job in workflow

### Note for Proprietary Software

Since py_template is proprietary software:
- **DO NOT** publish to public PyPI
- Use private package repository instead
- Or distribute via GitHub releases only

## Publishing to Private Repository

For proprietary software, use a private package repository:

### Option 1: GitHub Packages

```bash
# Configure pip to use GitHub Packages
pip install --index-url https://pypi.pkg.github.com/your-org/ py_template
```

### Option 2: Artifactory or Nexus

1. Set up your private repository
2. Add secrets to GitHub:
   - `PRIVATE_REPO_URL` - Your repository URL
   - `PRIVATE_REPO_USERNAME` - Username
   - `PRIVATE_REPO_PASSWORD` - Password/Token

3. Uncomment `publish-private` job in workflow

## Local Release Build

To build packages locally without releasing:

```bash
# Install build tools
uv add --dev build twine

# Build packages
uv run python -m build

# Check packages
uv run twine check dist/*

# View contents
tar -tzf dist/py_template-0.1.0.tar.gz
unzip -l dist/py_template-0.1.0-py3-none-any.whl
```

Built packages will be in `dist/` directory:
- `py_template-0.1.0.tar.gz` - Source distribution
- `py_template-0.1.0-py3-none-any.whl` - Wheel distribution

## Post-Release Checklist

After successful release:

- ✅ Verify GitHub release is created
- ✅ Download and test distribution packages
- ✅ Update documentation if needed
- ✅ Announce release (if applicable)
- ✅ Close related issues/PRs
- ✅ Plan next release

## Rollback

If you need to rollback a release:

### Remove GitHub Release

```bash
# Delete tag locally
git tag -d v0.2.0

# Delete tag on remote
git push origin :refs/tags/v0.2.0

# Delete release on GitHub UI
# Go to Releases → Click release → Delete
```

### Revert Code

```bash
# Revert to previous version
git revert <commit-hash>
git push origin main
```

## Troubleshooting

### Build Fails

**Issue**: Build job fails with dependency errors

**Solution**:
```bash
# Test build locally first
uv sync --extra dev
uv run python -m build
```

### Version Mismatch

**Issue**: Version in package doesn't match tag

**Solution**: Ensure `src/py_template/__version__.py` is updated before tagging

### Missing Changelog

**Issue**: Release has "See CHANGELOG.md for details"

**Solution**: Add version section to CHANGELOG.md:
```markdown
## [0.2.0] - YYYY-MM-DD

### Added
- New feature X
```

### Permission Denied

**Issue**: Workflow fails with permission error

**Solution**: Check repository settings → Actions → Workflow permissions → Enable write permissions

## Examples

### Example 1: Patch Release (Bug Fix)

```bash
# Fix bugs, commit changes
git add .
git commit -m "fix: resolve issue #123"

# Update version: 0.1.0 → 0.1.1
vim src/py_template/__version__.py

# Update changelog
vim CHANGELOG.md
# Add:
# ## [0.1.1] - YYYY-MM-DD
# ### Fixed
# - Resolve issue #123

# Commit and tag
git add src/py_template/__version__.py CHANGELOG.md
git commit -m "Bump version to 0.1.1"
git tag -a v0.1.1 -m "Release version 0.1.1"
git push origin main --tags
```

### Example 2: Minor Release (New Features)

```bash
# Develop features, commit changes
git add .
git commit -m "feat: add new transformer"

# Update version: 0.1.1 → 0.2.0
vim src/py_template/__version__.py

# Update changelog
vim CHANGELOG.md
# Add:
# ## [0.2.0] - YYYY-MM-DD
# ### Added
# - New transformer for data processing

# Commit and tag
git add src/py_template/__version__.py CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags
```

### Example 3: Major Release (Breaking Changes)

```bash
# Implement breaking changes
git add .
git commit -m "feat!: redesign API structure"

# Update version: 0.2.0 → 1.0.0
vim src/py_template/__version__.py

# Update changelog with migration guide
vim CHANGELOG.md
# Add:
# ## [1.0.0] - YYYY-MM-DD
# ### Changed (BREAKING)
# - Redesigned API structure
# ### Migration Guide
# - Update imports: old → new

# Commit and tag
git add src/py_template/__version__.py CHANGELOG.md
git commit -m "Bump version to 1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

## Best Practices

1. **Test Before Release**
   - Run full test suite
   - Test installation from built packages
   - Verify CLI commands work

2. **Document Changes**
   - Keep CHANGELOG.md up-to-date
   - Use conventional commit messages
   - Include migration guides for breaking changes

3. **Version Carefully**
   - Follow semantic versioning strictly
   - Never reuse version numbers
   - Use pre-release versions for testing

4. **Communication**
   - Announce releases to users
   - Provide upgrade instructions
   - Maintain release notes

5. **Automation**
   - Let CI/CD handle builds
   - Don't manually edit releases
   - Use consistent tagging conventions

## Resources

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Python Packaging](https://packaging.python.org/en/latest/)
