.PHONY: dev build test ci clean

dev:
	maturin develop

build:
	maturin build --release

test:
	uv run pytest

ci:
	maturin generate-ci github --platform windows --platform macos --platform linux -o .github/workflows/CI.yml

clean:
	cargo clean
	rm -rf target/ dist/ .pytest_cache/
