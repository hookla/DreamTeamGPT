.PHONY: fmt check style verify tests
fmt: ## Format code with isort and blace
	@echo "🚀 Formatting code: Running isort"
	@poetry run isort .
	@echo "🚀 Formatting code: Running black"
	@poetry run black .

check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
#	@echo "🚀 Static type checking: Running mypy -p dream_team_gpt"
#	@poetry run mypy -p dream_team_gpt

style: ## Run code style checks.
	@echo "🚀 Checking code formatting with isort: Running isort --check --diff ."
	@poetry run isort --check --diff .
	@echo "🚀 Checking code formatting with black: Running black --check --diff ."
	@poetry run black --check --diff .
#	@echo "🚀 Static type checking: Running mypy -p dream_team_gpt"
#	@poetry run mypy -p dream_team_gpt


test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest

verify: ## Run style and tests
	check
	style
	tests

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help