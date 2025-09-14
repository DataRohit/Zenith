# Zenith

<!-- Project Status -->
[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-brightgreen)](https://github.com/datarohit/zenith)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./license)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](#)
[![Coverage: 100%](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](./htmlcov/index.html)

<!-- Core Technologies -->
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3130/)
[![Typer](https://img.shields.io/badge/Typer-0.17.4-006B70.svg?logo=python&logoColor=white)](https://typer.tiangolo.com/)
[![Rich](https://img.shields.io/badge/Rich-1.8.1-darkblue.svg?logo=python&logoColor=white)](https://github.com/Textualize/rich)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.7.4-brightgreen.svg?logo=python&logoColor=white)](https://microsoft.github.io/autogen/)
[![Python-Dateutil](https://img.shields.io/badge/Python--Dateutil-2.9.0-blue.svg)](https://dateutil.readthedocs.io/en/stable/)
[![Python-Dotenv](https://img.shields.io/badge/Python--Dotenv-1.1.1-green.svg)](https://pypi.org/project/python-dotenv/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-424242.svg?logo=openai&logoColor=white)](https://openai.com/docs/api-reference/)

**A CLI-Based AI Coding Agent That Transforms Natural Language Into Efficient, Production-Ready Code.**

## 🌟 Features

### Core Features

-   **⚡ AI-Powered Code Generation**: Transform natural language instructions into high-quality, production-ready code.
-   **🗣️ Interactive Chat Interface**: Engage with Zenith through a rich, console-based chat experience.
-   **🔧 Extensible Toolset**: Utilizes a suite of file system tools (list, read, write, search, make directory, replace content) to interact with the codebase.
-   **⚙️ Flexible Configuration**: Easily configure OpenAI API keys, base URLs, and models via JSON or ENV files.
-   **🚀 Streaming Responses**: Provides real-time feedback from the AI agent through streaming.
-   **🛡️ Robust Error Handling**: Gracefully handles API errors (timeout, bad requests, not found) and file system issues.

### Development Tooling

-   **Ruff** Linting: Enforces code style and identifies potential issues.
-   **Pytest** + Coverage: Comprehensive testing framework with 100% coverage enforcement.

## 🛠️ Tech Stack

-   **Core**: Python 3.13
-   **CLI Framework**: Typer 0.17.4
-   **Rich Output**: Rich-cli 1.8.1
-   **AI Agent Framework**: Autogen-agentchat 0.7.4, Autogen-ext 0.7.4
-   **Date/Time Utilities**: Python-Dateutil 2.9.0
-   **Environment Variables**: Python-Dotenv 1.1.1
-   **AI API**: OpenAI API

## 🚀 Getting Started

### Prerequisites

-   Python 3.13
-   `pip` (Python package installer)
-   Git

### 1) Clone Repository

```bash
git clone https://github.com/DataRohit/Zenith.git
cd Zenith
```

### 2) Install Dependencies

```bash
pip install -e .
```

### 3) Configure Environment

Create a `.zenith/config.json` or `.zenith/.config.env` file in your project root.

**Example using `.zenith/config.json`:**

```json
{
    "zenith_openai_api_key": "YOUR_OPENAI_API_KEY",
    "zenith_openai_api_base": "https://api.openai.com/v1",
    "zenith_model": "gpt-4"
}
```

**Example using `.zenith/.config.env`:**

```env
ZENITH_OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
ZENITH_OPENAI_API_BASE="https://api.openai.com/v1"
ZENITH_MODEL="gpt-4"
```

Notes:

-   Keep secrets in `.env` or `config.json` files; do not commit them to version control.
-   If both `config.json` and `.config.env` exist in the `.zenith` directory, the application will raise an error.

### 4) Run Zenith

```bash
zenith chat
```

## ⚙️ Configuration Highlights

-   **`zenith_openai_api_key`**: Your OpenAI API key.
-   **`zenith_openai_api_base`**: The base URL for the OpenAI API. Defaults to `https://api.openai.com/v1`.
-   **`zenith_model`**: The specific model to be used (e.g., `gpt-4`, `gpt-3.5-turbo`).
-   **`zenith_assistant_description`**: A detailed description of the AI agent's capabilities.
-   **`zenith_assistant_system_message`**: The system-level instructions provided to the AI agent to guide its behavior.

These configurations are loaded via `zenith.utils.config_loader` and can be provided through a `.json` or `.env` file.

## 🧪 Development

Run Linting / Type Checking / Tests Locally:

```bash
make ruff-check  # or 'make ruff-lint' to auto-fix issues
pytest -q
```

-   Coverage Threshold Is Enforced At 100% Via `pytest.ini`.
-   HTML Coverage Report Is Generated At `htmlcov/index.html`.

Ruff and Pytest are configured in `pyproject.toml`.

## 📝 Makefile Commands

-   **help** — Show This Help Message
-   **Code Analysis:**
    -   `ruff-check` — Run Ruff Linter In Check Mode
    -   `ruff-lint` — Run Ruff Linter With Auto-Fix
-   **Cleaning:**
    -   `clean-all` — Remove Python And Tooling Artifacts

## 🔐 Environment Variables

Environment variables are loaded from `.zenith/config.json` or `.zenith/.config.env`.

**Critical:** Never commit sensitive values like API keys to version control.

## 📦 Dependencies

Pinned in `pyproject.toml` (and managed by `pip`). Key dependencies include:

-   `rich-cli`
-   `typer`
-   `python-dotenv`
-   `python-dateutil`
-   `autogen-agentchat`
-   `autogen-ext`
-   `autogen-ext[openai]`
-   `pytest` (dev)
-   `pytest-cov` (dev)
-   `pytest-asyncio` (dev)
-   `ruff` (dev)

## 📄 License

This Project Is Licensed Under The MIT License — See The [`license`](./license) File For Details.

## 📞 Contact

Rohit Ingole — <rohit.vilas.ingole@gmail.com>

Project Link: <https://github.com/DataRohit/Zenith>
