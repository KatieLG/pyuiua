.PHONY: dev build test ci clean

dev:
	maturin develop

build:
	maturin build --release

lint:
	uv run ruff check
	uv run ty check
	cargo check
	cargo clippy -- -D clippy::pedantic

test:
	uv run pytest

format:
	uv run ruff check --fix
	uv run ruff format
	cargo clippy --fix -- -D clippy::pedantic
	cargo format

check: format lint test
