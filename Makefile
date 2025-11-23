.PHONY: dev build test ci clean

dev:
	maturin develop

build:
	maturin build --release

lint:
	uv run ruff check
	cargo check
	cargo clippy


test:
	uv run pytest

format:
    uv run ruff check --fix
    uv run ruff format
	cargo format

check: format lint test
