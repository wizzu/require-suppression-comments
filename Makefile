SRC = require_suppression_comments.py

.PHONY: check lint format setup

setup:
	uv sync --extra dev

check: lint

lint:
	@echo "==> lint"
	uv run --extra dev ruff format --check $(SRC)
	uv run --extra dev ruff check $(SRC)
	uv run --extra dev bandit $(SRC) -q
	uv run --extra dev mypy $(SRC)
	python3 $(SRC) $(SRC)

format:
	@echo "==> format"
	uv run --extra dev ruff format $(SRC)
