.PHONY: fmt check style verify test help

fmt: ## Format code with ruff
	@echo "🚀 Formatting code: Running ruff format"
	@poetry run ruff format .
	@echo "🚀 Running linter auto-fixes: Running ruff check"
	@poetry run ruff check .

check: ## Run code quality tools
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "🚀 Static type checking: Running pyright"
	@poetry run pyright

style: ## Run code style checks
	@echo "🚀 Checking code with ruff linter: Running ruff check"
	@poetry run ruff check .
	@echo "🚀 Checking code formatting with ruff: Running ruff format --check"
	@poetry run ruff format --check .

test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest tests/

verify: ## Run check, style, and tests
	make check
	make style
	make test

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help