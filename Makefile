.PHONY: install dev test test-cov lint format ci migrate up down logs

install:
	pip install -e ".[dev]"

dev:
	uvicorn nuhoot.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -x -q

test-cov:
	pytest --cov=src/nuhoot --cov-report=html

lint:
	ruff check src/ tests/
	black --check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

ci: lint test
	@echo "CI pipeline passed"

migrate:
	alembic upgrade head

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f
