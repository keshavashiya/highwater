# highwater — Task Runner

default:
    @just --list

# Run exactly what CI runs
ci: lint fmtcheck test

# Lint
lint:
    uv run --locked ruff check .

# Check formatting
fmtcheck:
    uv run --locked ruff format --check .

# Format code
fmt:
    uv run ruff format .

# Run the tests
test:
    uv run --locked pytest
