# DreamTeamGPT Development Guidelines

## Dependency Management
- ALWAYS use Poetry for dependency management, NEVER pip
- `poetry install` - Install dependencies
- `poetry add package` - Add a new dependency
- `poetry add --dev package` - Add a development dependency
- `poetry update` - Update dependencies to latest versions

## Build & Test Commands
- `make fmt` - Format code with ruff (formats and applies auto-fixes)
- `make check` - Run pyright type checking
- `make style` - Check code formatting and linting
- `make test` - Run all tests
- `make verify` - Run check, style, and tests
- Single test: `poetry run pytest tests/test_file.py::TestClass::test_method -v`

## Code Style
- Python 3.11+
- Ruff for formatting and linting (99 character line length)
- Static typing with pyright (strict mode)
- Use descriptive error messages with proper exception types
- Imports: standard lib → third-party → local
- Naming: PEP 8 (CamelCase for classes, snake_case for functions/variables)
- Docstrings for public functions, classes, and modules
- Error handling: proper exception handling with logging via loguru
- Use type annotations for all function parameters and return values
- Test coverage expected for all new features

Format code before committing: `make fmt`