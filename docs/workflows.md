# GitHub Actions Workflows

This document provides an overview of all GitHub Actions workflows in the py_template project.

## Workflows Overview

| Workflow                               | Trigger            | Purpose              | Status Badge                                                                                |
| -------------------------------------- | ------------------ | -------------------- | ------------------------------------------------------------------------------------------- |
| [CI](#ci-workflow)                     | Push, PR           | Run tests and checks | ![CI](https://github.com/your-org/py_template/workflows/Continuous%20Integration/badge.svg) |
| [Code Quality](#code-quality-workflow) | Push, PR           | Code quality checks  | ![Code Quality](https://github.com/your-org/py_template/workflows/Code%20Quality/badge.svg) |
| [Security](#security-workflow)         | Push, PR, Schedule | Security scanning    | ![Security](https://github.com/your-org/py_template/workflows/Security%20Scan/badge.svg)    |
| [Release](#release-workflow)           | Tag push           | Build and release    | ![Release](https://github.com/your-org/py_template/workflows/Release/badge.svg)             |

---

## CI Workflow

**File:** [.github/workflows/ci.yml](../.github/workflows/ci.yml)

### Triggers

- **Push** to `main` or `dev` branches
- **Pull requests** to `main` or `dev` branches

### Jobs

#### 1. Test

- **Python versions:** 3.12
- **Steps:**
  1. Checkout code
  2. Install uv package manager
  3. Set up Python environment
  4. Install dependencies (dev + test)
  5. Run Ruff linting
  6. Run Ruff format check
  7. Run pytest with coverage
  8. Upload coverage to Codecov

### Usage

This workflow runs automatically on every push and PR. No manual intervention needed.

### Skipping CI

To skip CI for a commit (e.g., documentation changes):

```bash
git commit -m "docs: update README [skip ci]"
```

---

## Code Quality Workflow

**File:** [.github/workflows/code-quality.yml](../.github/workflows/code-quality.yml)

### Triggers

- **Push** to `main` or `dev` branches
- **Pull requests** to `main` or `dev` branches

### Jobs

#### 1. Code Quality

- **Steps:**
  1. Checkout code
  2. Run Ruff linting (output to GitHub)
  3. Run Ruff format check with diff

### Usage

Provides quick code quality feedback without full test suite. Runs in parallel with CI workflow.

### Note

This workflow has some overlap with the CI workflow. Consider consolidating if maintenance becomes an issue.

---

## Security Workflow

**File:** [.github/workflows/security.yml](../.github/workflows/security.yml)

### Triggers

- **Push** to `main` or `dev` branches
- **Pull requests** to `main` or `dev` branches
- **Schedule:** Weekly on Monday at 00:00 UTC

### Jobs

#### 1. Security Scan

- **Permissions:** security-events (write), contents (read)
- **Steps:**
  1. Checkout code
  2. Install uv and Python
  3. Install dependencies
  4. Run Bandit security scanner
  5. Run Safety dependency checker
  6. Upload security reports as artifacts

### Usage

**Automatic:** Runs on every push/PR and weekly.

**Manual trigger:**

1. Go to Actions → Security Scan
2. Click "Run workflow"
3. Select branch
4. Click "Run workflow"

### Viewing Reports

Security reports are available as artifacts:

1. Go to Actions → Select workflow run
2. Scroll to "Artifacts" section
3. Download `bandit-report`

### Findings

Review security findings and address vulnerabilities:

```bash
# Install security tools locally
uv add --dev bandit[toml] safety

# Run Bandit
uv run bandit -r src/

# Run Safety
uv run safety check
```

---

## Release Workflow

**File:** [.github/workflows/release.yml](../.github/workflows/release.yml)

### Triggers

#### 1. Tag Push (Recommended)

```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

#### 2. Manual Workflow Dispatch

- Go to Actions → Release
- Click "Run workflow"
- Enter version number (without 'v')

### Jobs

#### 1. Build Distribution

- Build source distribution (`.tar.gz`)
- Build wheel distribution (`.whl`)
- Validate packages with `twine check`
- Upload artifacts

#### 2. Publish GitHub Release

- Create GitHub release
- Extract changelog from CHANGELOG.md
- Upload distribution files
- Tag release

#### 3. Publish to PyPI (Optional, Commented)

- Publish to PyPI
- **Requires:** `PYPI_API_TOKEN` secret

#### 4. Publish to Private Repository (Optional, Commented)

- Publish to private package repository
- **Requires:** Repository URL and credentials

#### 5. Notify

- Generate release summary
- Update GitHub Step Summary
- Send notifications (if configured)

### Release Process

See [Release Process Guide](release.md) for detailed instructions.

#### Quick Release

```bash
# 1. Update version
vim src/py_template/__version__.py

# 2. Update changelog
vim CHANGELOG.md

# 3. Commit and tag
git add .
git commit -m "Bump version to 0.2.0"
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags
```

### Distribution Options

The workflow supports multiple distribution methods:

1. **GitHub Releases** (Default, enabled)
   - Free for public and private repos
   - Easy to download
   - Good for proprietary software

2. **PyPI** (Optional, commented out)
   - Public package index
   - Use only for open-source projects
   - **DO NOT enable for proprietary software**

3. **Private Repository** (Optional, commented out)
   - Artifactory, Nexus, or similar
   - Good for enterprise deployments
   - Requires setup and credentials

### Enabling PyPI Publishing

**⚠️ Warning:** Only for open-source projects

1. Uncomment `publish-pypi` job in workflow
2. Create PyPI API token
3. Add `PYPI_API_TOKEN` to GitHub Secrets

### Enabling Private Repository

1. Uncomment `publish-private` job in workflow
2. Set up private repository
3. Add secrets:
   - `PRIVATE_REPO_URL`
   - `PRIVATE_REPO_USERNAME`
   - `PRIVATE_REPO_PASSWORD`

---

## Workflow Best Practices

### 1. Keep Workflows Fast

- Use caching for dependencies
- Run jobs in parallel when possible
- Skip unnecessary steps

### 2. Use Matrix Strategy

For testing multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']
```

### 3. Fail Fast

Set `fail-fast: false` to see all failures:

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ['3.11', '3.12']
```

### 4. Use Conditionals

Skip steps based on conditions:

```yaml
- name: Upload coverage
  if: matrix.python-version == '3.12'
  uses: codecov/codecov-action@v4
```

### 5. Secrets Management

- Never commit secrets to code
- Use GitHub Secrets for sensitive data
- Rotate secrets regularly

### 6. Workflow Permissions

Grant minimum required permissions:

```yaml
permissions:
  contents: read
  pull-requests: write
```

---

## Troubleshooting

### Workflow Not Triggering

**Problem:** Workflow doesn't run on push/PR

**Solutions:**

1. Check workflow file syntax (YAML)
2. Verify trigger configuration matches branch name
3. Check repository permissions
4. Look for `[skip ci]` in commit message

### Build Fails

**Problem:** Build job fails

**Solutions:**

1. Test locally first: `uv run python -m build`
2. Check dependency versions
3. Review error logs in Actions tab
4. Ensure uv.lock is up-to-date

### Permission Denied

**Problem:** Workflow fails with permission error

**Solutions:**

1. Check Settings → Actions → Workflow permissions
2. Enable "Read and write permissions"
3. Add explicit permissions in workflow file

### Secret Not Found

**Problem:** Secret is undefined

**Solutions:**

1. Verify secret name matches exactly
2. Check repository vs organization secrets
3. Ensure secret is set in correct repository

### Coverage Upload Fails

**Problem:** Codecov upload fails

**Solutions:**

1. Check Codecov token in secrets
2. Verify coverage.xml is generated
3. Review Codecov integration status

---

## Monitoring and Maintenance

### Viewing Workflow Runs

1. Go to repository → Actions tab
2. Select workflow from sidebar
3. View recent runs and their status

### Workflow Insights

View workflow insights:

1. Actions → Select workflow
2. Click "..." → View workflow insights
3. See success rate, duration trends

### Updating Workflows

When updating workflows:

1. Test changes on a feature branch first
2. Use workflow dispatch for testing
3. Monitor first runs after changes
4. Keep workflows documented

### Dependency Updates

Keep workflow actions up-to-date:

```yaml
# Good - use specific version
- uses: actions/checkout@v4

# Avoid - using latest can break
- uses: actions/checkout@latest
```

Update action versions periodically:

1. Check for new releases
2. Review changelogs
3. Test in feature branch
4. Update and monitor

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Available Actions](https://github.com/marketplace?type=actions)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/guides/best-practices)

---

## Quick Reference Commands

```bash
# View workflow status
gh workflow list
gh workflow view ci.yml

# Run workflow manually
gh workflow run release.yml

# View workflow runs
gh run list --workflow=ci.yml
gh run view <run-id>

# Download artifacts
gh run download <run-id>

# Re-run failed jobs
gh run rerun <run-id> --failed
```

## Workflow Status Badges

Add to README.md:

```markdown
![CI](https://github.com/your-org/py_template/workflows/Continuous%20Integration/badge.svg)
![Security](https://github.com/your-org/py_template/workflows/Security%20Scan/badge.svg)
![Release](https://github.com/your-org/py_template/workflows/Release/badge.svg)
```
