# Python 项目标准化文档

本文档定义了现代 Python 项目的开发标准、工具配置和最佳实践，旨在确保代码质量、团队协作效率和项目可维护性。适用于任何 Python 项目的标准化开发流程。

## 目录

1. [项目概述](#项目概述)
2. [目录结构标准](#目录结构标准)
3. [包管理与依赖管理](#包管理与依赖管理)
4. [代码格式化工具链](#代码格式化工具链)
5. [开发环境配置](#开发环境配置)
6. [质量保证体系](#质量保证体系)
7. [DevOps 工作流](#devops-工作流)
8. [容器化与部署](#容器化与部署)
9. [开发规范](#开发规范)
10. [常用命令参考](#常用命令参考)

## 项目概述

本标准适用于现代 Python 项目，无论是 Web 应用、API 服务、数据科学项目还是命令行工具。

### 核心工具链

- **编程语言**: Python 3.11+ (推荐 3.12)
- **包管理**: uv (现代 Python 包管理器)
- **代码质量**: Ruff (linting + formatting)
- **测试框架**: pytest
- **类型检查**: mypy (可选)
- **容器化**: Docker
- **文档**: Sphinx (可选)

## 目录结构标准

### Python 项目标准布局

本项目采用现代 Python 项目的 **src 布局模式**，符合 PEP 518 和社区最佳实践：

```
my-python-project/
├── .github/                    # GitHub 配置
│   └── workflows/              # CI/CD 工作流
│       ├── ci.yml              # 持续集成
│       ├── security.yml        # 安全扫描
│       └── release.yml         # 自动发布
├── .vscode/                    # VSCode 配置
│   ├── settings.json           # 编辑器设置
│   ├── extensions.json         # 推荐扩展
│   └── launch.json             # 调试配置
├── docs/                       # 项目文档
│   ├── api.md                  # API 文档
│   ├── development.md          # 开发指南
│   └── deployment.md           # 部署说明
├── src/                        # 源代码目录
│   └── <your-package>/         # 主包
│       ├── __init__.py         # 包初始化
│       ├── main.py             # 应用入口
│       ├── config/             # 配置模块
│       │   ├── __init__.py
│       │   └── settings.py     # 配置和设置
│       ├── core/               # 核心功能
│       │   ├── __init__.py
│       │   ├── models.py       # 数据模型
│       │   ├── exceptions.py   # 自定义异常
│       │   └── *.py            # 其他核心模块
│       ├── services/           # 业务服务层
│       │   ├── __init__.py
│       │   ├── base.py         # 基础服务类
│       │   └── *.py            # 具体业务服务
│       ├── api/                # API 层 (Web项目)
│       │   ├── __init__.py
│       │   ├── routes.py       # 路由定义
│       │   └── handlers.py     # 请求处理器
│       ├── cli/                # 命令行接口 (CLI项目)
│       │   ├── __init__.py
│       │   └── commands.py     # 命令定义
│       └── utils/              # 工具模块
│           ├── __init__.py
│           ├── helpers.py      # 辅助函数
│           └── logging.py      # 日志配置
├── tests/                      # 测试文件
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置
│   ├── unit/                   # 单元测试
│   │   └── test_*.py
│   └── integration/            # 集成测试
│       └── test_*.py
├── scripts/                    # 脚本文件
│   ├── setup.sh                # 环境设置
│   └── deploy.sh               # 部署脚本
├── .gitignore                  # Git 忽略文件
├── .pre-commit-config.yaml     # Pre-commit 配置
├── .prettierrc                 # Prettier 配置
├── .editorconfig               # 编辑器配置
├── Dockerfile                  # Docker 构建文件
├── docker-compose.yml          # Docker Compose 配置
├── pyproject.toml              # 项目配置和依赖
├── uv.lock                     # 依赖锁定文件
├── README.md                   # 项目说明
├── CHANGELOG.md                # 更新日志
├── LICENSE                     # 许可证
└── .env.example                # 环境变量模板
```

### 目录职责说明

#### **src/ 布局的优势**

1. **包导入清晰**: 避免测试时的包导入冲突
2. **打包友好**: 符合现代 Python 打包标准
3. **IDE 支持**: 更好的 IDE 集成和类型检查
4. **测试隔离**: 测试代码与源码完全分离

#### **核心目录职责**

- **config/**: 应用配置、环境变量管理
- **core/**: 核心业务逻辑，不依赖外部服务
- **services/**: 业务服务层，每个服务负责特定功能域
- **api/**: API 路由和请求处理（Web 项目）
- **cli/**: 命令行接口（CLI 项目）
- **utils/**: 通用工具函数，可被多个模块使用
- **models/**: 数据模型和业务实体

## 包管理与依赖管理

### uv: 现代 Python 包管理器

本项目使用 **uv** 作为包管理工具，提供快速、可靠的依赖管理。

#### uv 优势

- **极快的依赖解析**: 比 pip 快 10-100 倍
- **兼容性强**: 完全兼容 pip 和 PyPI
- **现代化**: 支持 PEP 621 标准和现代 Python 工作流
- **虚拟环境管理**: 自动管理项目虚拟环境

#### 基本命令

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装所有依赖（包括开发依赖）
uv sync

# 仅安装生产依赖
uv sync --no-dev

# 添加新依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 运行命令（自动激活虚拟环境）
uv run python run.py
uv run pytest
```

### pyproject.toml 配置

项目使用 **pyproject.toml** 作为唯一的配置文件，遵循 PEP 518/621 标准。以下是完整的配置模板：

```toml
# ============================================================================
# 项目元数据配置
# ============================================================================
[project]
name = "<your-package-name>"
version = "<your-version>"              # 如: "0.1.0" 或使用 dynamic = ["version"]
description = "<your-project-description>"
readme = "README.md"                   # 或 "README.rst"
requires-python = ">=<your-min-python-version>"  # 如: ">=3.11"
license = {text = "<your-license>"}     # MIT, Apache-2.0, GPL-3.0, BSD-3-Clause 等
authors = [
    {name = "<your-name>", email = "<your-email@example.com>"},
    # 可以有多个作者
]
maintainers = [
    {name = "<maintainer-name>", email = "<maintainer-email@example.com>"},
]
keywords = ["<keyword1>", "<keyword2>", "<keyword3>"]  # 项目关键词
classifiers = [
    # 开发状态
    "Development Status :: <your-dev-status>",  # 1-Planning, 2-Pre-Alpha, 3-Alpha, 4-Beta, 5-Production/Stable
    # 目标受众
    "Intended Audience :: <your-audience>",     # Developers, End Users/Desktop, Science/Research 等
    # 许可证
    "License :: OSI Approved :: <your-license-classifier>",
    # 操作系统
    "Operating System :: OS Independent",        # 或特定操作系统
    # 编程语言
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.<your-min-version>",
    "Programming Language :: Python :: 3.<your-max-version>",
    # 主题
    "Topic :: <your-topic>",                    # Software Development, Scientific/Engineering 等
]

# ============================================================================
# 项目 URLs
# ============================================================================
[project.urls]
Homepage = "https://github.com/<your-username>/<your-repo>"
Documentation = "https://<your-docs-url>"        # 如: ReadTheDocs, GitHub Pages
"Bug Tracker" = "https://github.com/<your-username>/<your-repo>/issues"
"Source Code" = "https://github.com/<your-username>/<your-repo>"
Changelog = "https://github.com/<your-username>/<your-repo>/blob/main/CHANGELOG.md"
"Funding" = "https://github.com/sponsors/<your-username>"  # 可选
"Download" = "https://pypi.org/project/<your-package-name>/"  # 可选

# ============================================================================
# 依赖管理
# ============================================================================
# 生产依赖
dependencies = [
    "<your-production-dependency>>=<version>",
]

# ============================================================================
# 可选依赖组
# ============================================================================
[project.optional-dependencies]
# 测试依赖
test = [
    "<your-test-dependency>>=<version>",
]

# 开发依赖
dev = [
    "<your-dev-dependency>>=<version>",
]

# 文档依赖
docs = [
    "<your-doc-dependency>>=<version>",
]

# 性能分析
profile = [
    "<your-profile-dependency>>=<version>",

]

# 类型检查相关
typing = [
    "<your-typing-dependency>>=<version>",
]

# 完整开发环境（包含所有可选依赖）
all = [
    "<your-package-name>[test,dev,docs,profile,typing]"
]

# ============================================================================
# 控制台脚本（CLI 项目）
# ============================================================================
[project.scripts]
# <your-cli-name> = "<your-package>.cli:main"
# <your-cli-name>-admin = "<your-package>.cli.admin:main"
# 示例:
# myapp = "mypackage.cli:main"
# myapp-dev = "mypackage.cli:dev_main"
# myapp-migrate = "mypackage.db:migrate"

# GUI 脚本（桌面应用）
[project.gui-scripts]
# <your-gui-name> = "<your-package>.gui:main"

# ============================================================================
# 构建系统配置
# ============================================================================
[build-system]
requires = ["<your-build-backend>>=<version>"]
# 常用选项:
# "hatchling>=1.18.0"           # Hatch 构建后端（推荐）
# "setuptools>=64", "wheel"     # 传统 setuptools
# "flit_core>=3.2"              # Flit 构建后端
# "poetry-core>=1.0.0"          # Poetry 构建后端

build-backend = "<your-build-backend-module>"
# 对应的后端模块:
# "hatchling.build"             # 对应 hatchling
# "setuptools.build_meta"       # 对应 setuptools
# "flit_core.buildapi"          # 对应 flit_core
# "poetry.core.masonry.api"     # 对应 poetry-core

# ============================================================================
# Hatchling 配置（如果使用 hatchling）
# ============================================================================
[tool.hatch.version]
# 选项 1: 从代码文件获取版本
path = "src/<your-package>/__init__.py"
pattern = "__version__ = ['\"](?P<version>[^'\"]*)['\"]"    # 版本号正则匹配

# 选项 2: 从 git 标签获取版本
# source = "vcs"
# raw-options = { local_scheme = "no-local-version" }

# 选项 3: 使用固定版本（在 [project] 中设置 version）

[tool.hatch.build.targets.wheel]
# 指定要打包的目录
packages = ["src/<your-package>"]

# 排除文件和目录
exclude = [
    "/.github",
    "/docs",
    "/tests",
    "/scripts",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "__pycache__",
    ".DS_Store",
    "*.egg-info",
]

[tool.hatch.build.targets.sdist]
# 源码分发包含的文件
include = [
    "/src",
    "/tests",
    "/docs",
    "/README.md",
    "/LICENSE",
    "/CHANGELOG.md",
    "/pyproject.toml",
    # 可能还需要的文件
    # "/requirements*.txt",
    # "/Makefile",
    # "/.github/workflows",
]

# 排除文件
exclude = [
    "/.venv",
    "/dist",
    "/.mypy_cache",
    "/.pytest_cache",
    "/.ruff_cache",
    "__pycache__",
]
```

#### pyproject.toml 配置说明

**核心配置要点**：

1. **项目元数据**: 完整填写项目信息，有助于包的发现和使用
2. **版本管理**: 推荐使用动态版本，从代码或 git 标签获取
3. **依赖管理**: 使用语义化版本约束，避免过于严格的版本锁定
4. **可选依赖**: 按功能分组，便于不同环境的安装
5. **构建配置**: 正确设置包含和排除的文件

**版本约束建议**：

```toml
# 推荐：允许兼容更新
"package>=1.0.0,<2.0.0"    # 或简写为 "package~=1.0"

# 避免：过于严格的版本锁定
"package==1.0.0"           # 除非有特殊原因

# 避免：过于宽松的约束
"package"                  # 可能导致不兼容问题
```

**常用命令示例**：

```bash
# 安装不同的依赖组
uv sync                      # 仅安装生产依赖
uv sync --extra dev          # 安装开发依赖
uv sync --extra test         # 安装测试依赖
uv sync --extra all          # 安装所有可选依赖

# 使用 dependency-groups（uv 现代语法）
uv sync --group dev          # 安装开发组
uv sync --group test         # 安装测试组
```

## 代码格式化工具链

### Python 代码: Ruff

**Ruff** 是一个极速的 Python linter 和 formatter，集成了多种工具功能。

#### Ruff 配置

```toml
[tool.ruff]
target-version = "py312"              # Python 版本
line-length = 100                     # 行长度限制
src = ["src", "tests"]                # 源码目录

[tool.ruff.lint]
select = [
    "E", "W",      # pycodestyle
    "F",           # pyflakes
    "I",           # isort
    "B",           # flake8-bugbear
    "C4",          # flake8-comprehensions
    "UP",          # pyupgrade
    "SIM",         # flake8-simplify
    "PIE",         # flake8-pie
    "RET",         # flake8-return
    "ARG",         # flake8-unused-arguments
    "PTH",         # flake8-use-pathlib
]

fixable = ["ALL"]                     # 自动修复所有可修复问题
```

#### 常用命令

```bash
# 代码格式化
uv run ruff format

# 代码检查
uv run ruff check

# 自动修复
uv run ruff check --fix

# 完整检查和格式化
uv run ruff check --fix && uv run ruff format
```

### Markdown 和配置文件: Prettier

**Prettier** 用于格式化 Markdown、YAML、JSON 等非 Python 文件。

#### .prettierrc 配置

```json
{
  "tabWidth": 4,
  "useTabs": true,
  "printWidth": 120,
  "singleQuote": true,
  "proseWrap": "preserve",
  "overrides": [
    {
      "files": ["*.json", "*.jsonc"],
      "options": {
        "trailingComma": "none"
      }
    },
    {
      "files": "manifest.json",
      "options": {
        "parser": "jsonc"
      }
    }
  ]
}
```

#### 支持的文件类型

- **Markdown**: `*.md`, `*.mdx`
- **YAML**: `*.yml`, `*.yaml`
- **JSON**: `*.json`
- **配置文件**: `.prettierrc`, `.github/workflows/*.yml`

### EditorConfig 配置

创建 `.editorconfig` 文件统一编辑器行为：

```ini
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = tab
indent_size = 4

# JSON files use tab indentation
[*.json]
indent_style = tab
indent_size = 4

# YAML files use tab indentation
[*.{yml,yaml}]
indent_style = tab
indent_size = 4

# Markdown files
[*.md]
trim_trailing_whitespace = false
```

## 开发环境配置

### VSCode 配置

#### settings.json

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "files.associations": {
    "*.mdc": "markdown",
    "*.env*": "dotenv"
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.terminal.activateEnvironment": true
}
```

#### 推荐扩展 (extensions.json)

```json
{
  "recommendations": [
    "charliermarsh.ruff", // Python linting/formatting
    "ms-python.python", // Python 支持
    "ms-python.pylance", // Python 语言服务器
    "ms-python.pytest", // pytest 支持
    "esbenp.prettier-vscode", // Prettier 格式化
    "tamasfe.even-better-toml", // TOML 支持
    "redhat.vscode-yaml", // YAML 支持
    "ms-vscode.vscode-json", // JSON 支持
    "GitHub.vscode-pull-request-github" // GitHub 集成
  ]
}
```

#### 调试配置 (launch.json)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run AlgPoints Server",
      "type": "python",
      "request": "launch",
      "program": "run.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    }
  ]
}
```

## 质量保证体系

### Pre-commit Hooks

自动化代码质量检查，在每次提交前运行：

#### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.13.2
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
```

#### 使用方法

```bash
# 安装 pre-commit hooks
uv run pre-commit install

# 手动运行所有文件检查
uv run pre-commit run --all-files

# 绕过 hooks（紧急情况）
git commit --no-verify -m "emergency commit"
```

### 测试框架: pytest

#### pytest 配置

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --showlocals --durations=10"
asyncio_mode = "auto"                    # 自动异步支持
log_cli = true
log_cli_level = "DEBUG"
```

#### 测试命令

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_chat.py

# 运行带覆盖率的测试
uv run pytest --cov=src

# 生成 HTML 覆盖率报告
uv run pytest --cov=src --cov-report=html
```

### 代码覆盖率

#### coverage 配置

```toml
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
```

## DevOps 工作流

### CI/CD 流程设计

#### 1. 持续集成 (CI)

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v2

      - name: Set up Python
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

#### 2. 安全扫描

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Bandit security scan
        run: uv run bandit -r src/

      - name: Run Safety dependency check
        run: uv run safety check
```

#### 3. 容器构建

```yaml
# .github/workflows/docker.yml
name: Docker Build

on:
  push:
    tags: ['v*']
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t <your-app>:latest .

      - name: Push to registry
        # 推送到容器仓库
```

### 分支管理策略

#### 提交规范

```
type(scope): description

# 类型
feat:     新功能
fix:      bug 修复
docs:     文档更新
style:    代码格式（不影响代码运行）
refactor: 重构
test:     测试
chore:    构建过程或辅助工具的变动

# 示例
feat(chat): add streaming response support
fix(api): handle empty message validation
docs(readme): update installation instructions
```

### 版本发布策略

#### 语义化版本控制

```
MAJOR.MINOR.PATCH

MAJOR: 不兼容的 API 修改
MINOR: 向下兼容的功能性新增
PATCH: 向下兼容的问题修正
```

#### 自动化发布

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Build and release
        # 自动构建和发布
```

## 容器化与部署

### Docker 配置

#### Dockerfile 最佳实践

```dockerfile
# 多阶段构建，优化镜像大小
FROM python:3.12-slim as builder

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

WORKDIR /app

# 依赖层（利用缓存）
COPY pyproject.toml uv.lock* ./
COPY src/<your-package>/__init__.py ./src/<your-package>/__init__.py

# 安装依赖
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 运行时阶段
FROM python:3.12-slim

WORKDIR /app

# 复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 复制源码
COPY src/ ./src/

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# 健康检查（Web 应用）
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "<your-package>.main"]
```

#### Docker Compose 开发环境

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - '8080:8080'
    environment:
      - PYTHONPATH=/app/src
      - DEBUG=true
    volumes:
      - ./src:/app/src:ro
      - ./tests:/app/tests:ro
    command: uv run python -m <your-package>.main --reload
```

### 环境变量管理

#### .env 文件模板

```bash
# .env.example
# 复制为 .env 并填入实际值

# 应用配置
APP_NAME=my-app
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
PORT=8080

# 数据库配置（如果使用）
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
REDIS_URL=redis://localhost:6379/0

# 外部服务（根据需要）
API_KEY=your-api-key
SECRET_KEY=your-secret-key
```

### Kubernetes 部署

#### 基本部署配置

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
```

## 开发规范

### 代码风格

#### Python 代码规范

1. **遵循 PEP 8**: 使用 Ruff 自动格式化
2. **行长度**: 最大 100 字符
3. **导入顺序**: 标准库 → 第三方库 → 本地导入
4. **类型注解**: 推荐使用类型提示

```python
# 好的示例
from typing import Optional, List
import logging

from pydantic import BaseModel

from <your-package>.core.models import User
from <your-package>.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserRequest(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


def create_user(user_data: UserRequest) -> dict:
    """创建新用户"""
    try:
        user_service = UserService()
        user = user_service.create(user_data.model_dump())
        logger.info(f"用户创建成功: {user.id}")
        return {"status": "success", "user_id": user.id}
    except ValueError as e:
        logger.error(f"用户创建失败: {e}")
        return {"status": "error", "message": str(e)}
```

#### 命名规范

- **文件名**: `snake_case.py`
- **类名**: `PascalCase`
- **函数/变量**: `snake_case`
- **常量**: `UPPER_SNAKE_CASE`
- **私有方法**: `_leading_underscore`

### 文档规范

#### Docstring 格式

```python
def process_message(message: str, user_id: int) -> dict:
    """处理用户消息并返回响应

    Args:
        message: 用户输入的消息内容
        user_id: 用户唯一标识符

    Returns:
        包含响应内容和状态的字典

    Raises:
        ValueError: 当消息为空时抛出
        ConnectionError: 当AI服务不可用时抛出
    """
    # 实现代码
```

#### README 结构

```markdown
# 项目名称

简短描述

## 快速开始

### 安装

### 运行

### 基本使用

## 功能特性

## API 文档

## 开发指南

## 贡献指南

## 许可证
```

### 错误处理规范

#### 异常处理策略

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def call_external_service(data: dict) -> Optional[dict]:
    """调用外部服务的示例"""
    try:
        # 外部服务调用
        response = await external_client.post(data)
        return response.json()

    except ConnectionError as e:
        logger.error(f"外部服务连接失败: {e}")
        # 降级策略
        return {"error": "服务暂时不可用，请稍后重试"}

    except ValueError as e:
        logger.warning(f"数据验证失败: {e}")
        return None

    except Exception as e:
        logger.exception(f"未预期的错误: {e}")
        raise
```

## 常用命令参考

### 项目设置

```bash
# 初始设置
git clone <repository>
cd my-python-project
uv sync
uv run pre-commit install

# 验证设置
uv run python -m <your-package>.main  # 或其他入口
uv run pytest
```

### 日常开发

```bash
# 启动应用（根据项目类型调整）
uv run python -m <your-package>.main

# 代码质量检查
uv run ruff check --fix && uv run ruff format

# 运行测试
uv run pytest -v

# 运行测试并查看覆盖率
uv run pytest --cov=src --cov-report=html
```

### 依赖管理

```bash
# 添加生产依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 更新依赖
uv sync --upgrade

# 查看依赖树
uv tree
```

### Git 工作流

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交更改（自动运行 pre-commit）
git add .
git commit -m "feat: add new feature"

# 推送并创建 PR
git push origin feature/new-feature
```

### Docker 操作

```bash
# 构建镜像
docker build -t my-app:latest .

# 运行容器
docker run -p 8080:8080 my-app:latest

# 开发环境
docker-compose -f docker-compose.dev.yml up
```

---

## 总结

本文档定义了现代 Python 项目的完整开发标准，涵盖了从代码编写到部署的各个环节。遵循这些标准将确保：

- **代码质量**: 统一的格式化和质量检查
- **开发效率**: 现代化工具链和自动化流程
- **团队协作**: 清晰的规范和工作流程
- **项目可维护性**: 标准化的结构和文档

### 重要提醒

1. **严格遵循 Ruff 配置**: 确保代码风格一致性
2. **使用 uv 管理依赖**: 享受快速、可靠的包管理
3. **编写测试**: 确保代码质量和功能稳定性
4. **保持文档更新**: 与代码同步更新文档
5. **遵循 Git 规范**: 使用规范的提交消息和分支策略

对于任何疑问或改进建议，请通过 Issue 或 Pull Request 与团队讨论。
