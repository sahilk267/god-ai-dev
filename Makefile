.PHONY: help install dev build deploy test clean

help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make dev       - Run development server (uvicorn on :8000)"
	@echo "  make build     - Build Docker images (docker compose build)"
	@echo "  make deploy    - Deploy to production (scripts/deploy.sh)"
	@echo "  make test      - Run tests"
	@echo "  make clean     - Clean temporary files"
	@echo ""
	@echo "Docs: docs/implementation-plan.md (pipeline + IDE checklist)"
	@echo "      api architechture.md, deployment architechture.md"

install:
	pip install -r requirements.txt

dev:
	uvicorn backend.api.routes:app --reload --port 8000

build:
	docker compose build

deploy:
	bash scripts/deploy.sh

test:
	pytest test/ -v --cov=backend

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
