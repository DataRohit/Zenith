# Cross-Platform Color Definitions
ifeq ($(OS),Windows_NT)
    # Git Bash Support Only
    ifeq ($(shell echo $$BASH_VERSION 2>/dev/null),)
        $(error This Makefile Only Supports Git Bash On Windows!)
    endif
    GREEN=\033[0;32m
    BLUE=\033[0;34m
    YELLOW=\033[1;33m
    RED=\033[0;31m
    NC=\033[0m
else
    # Unix Systems Have Full ANSI Color Support
    GREEN=\033[0;32m
    BLUE=\033[0;34m
    YELLOW=\033[1;33m
    RED=\033[0;31m
    NC=\033[0m
endif

# Default Goal
.DEFAULT_GOAL := help

# Utility Echo And Color Variable Aliases
ECHO_CMD=echo
GREEN_START=${GREEN}
BLUE_START=${BLUE}
YELLOW_START=${YELLOW}
RED_START=${RED}
COLOR_END=${NC}

# Help Target: Show Available Makefile Commands
help:
	@echo ""
	@printf "${BLUE}Zenith Makefile Commands${NC}\n"
	@echo ""
	@printf "${GREEN}General:${NC}\n"
	@echo "  help            - Show This Help Message"
	@echo ""
	@printf "${GREEN}Code Analysis:${NC}\n"
	@echo "  ruff-check      - Run Ruff Linter In Check Mode"
	@echo "  ruff-lint       - Run Ruff Linter With Auto-Fix"
	@echo ""
	@printf "${GREEN}Cleaning:${NC}\n"
	@echo "  clean-all       - Remove Python And Tooling Artifacts"
	@echo ""

# Ruff-Check Target: Run Ruff Linter In Check Mode
ruff-check:
	@echo ""
	@printf "${YELLOW}Running Ruff Linter In Check Mode...${NC}\n"
	ruff check .
	@printf "${GREEN}Ruff Check Completed!${NC}\n"
	@echo ""

# Ruff-Lint Target: Run Ruff Linter With Auto-Fix
ruff-lint:
	@echo ""
	@printf "${YELLOW}Running Ruff Linter With Auto-Fix...${NC}\n"
	ruff check --fix .
	@printf "${GREEN}Ruff Lint Completed!${NC}\n"
	@echo ""

# Clean-All Target: Remove Python And Tooling Artifacts
clean-all:
	@echo ""
	@printf "${YELLOW}Cleaning All Python And Tooling Artifacts...${NC}\n"
	find . -type d -name 'build' -prune -exec rm -rf {} + || true
	find . -type d -name 'dist' -prune -exec rm -rf {} + || true
	find . -type d -name 'sdist' -prune -exec rm -rf {} + || true
	find . -type d -name 'wheels' -prune -exec rm -rf {} + || true
	find . -type d -name '*.egg-info' -prune -exec rm -rf {} + || true
	find . -type d -name 'pip-wheel-metadata' -prune -exec rm -rf {} + || true
	find . -type d -name '__pycache__' -prune -exec rm -rf {} + || true
	find . -type d -name '.pytest_cache' -prune -exec rm -rf {} + || true
	find . -type d -name '.mypy_cache' -prune -exec rm -rf {} + || true
	find . -type d -name '.ruff_cache' -prune -exec rm -rf {} + || true
	find . -type d -name '.tox' -prune -exec rm -rf {} + || true
	find . -type d -name '.nox' -prune -exec rm -rf {} + || true
	find . -type d -name '.cache' -prune -exec rm -rf {} + || true
	find . -type d -name 'htmlcov' -prune -exec rm -rf {} + || true
	find . -type d -name '.scannerwork' -prune -exec rm -rf {} + || true
	find . -type f -name '.coverage' -exec rm -f {} \; || true
	find . -type f -name '.coverage.*' -delete || true
	find . -type f -name 'coverage.xml' -delete || true
	find . -type d -name 'coverage' -prune -exec rm -rf {} + || true
	find . -type f -name '*.pyc' -delete || true
	find . -type f -name '*.pyo' -delete || true
	@printf "${GREEN}Cleanup Completed Successfully!${NC}\n"
	@echo ""

# Phony Targets Declaration
.PHONY: help ruff-check ruff-lint clean-all
