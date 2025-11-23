.PHONY: dev build test ci clean

dev:
	maturin develop

build:
	maturin build --release

test:
	uv run pytest

format:
    uv run ruff check --fix
    uv run ruff format

check: format test
