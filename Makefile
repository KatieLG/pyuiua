.PHONY: dev build lint test format check test-release release

dev:
	maturin develop

build:
	maturin build --release

lint:
	ruff check
	ty check
	cargo check
	cargo clippy -- -D clippy::pedantic

test:
	pytest

format:
	ruff check --fix
	ruff format
	cargo clippy --fix --allow-dirty -- -D clippy::pedantic 
	cargo fmt

check: format lint test

test-release:
	maturin publish --repository testpypi

release:
	maturin publish
