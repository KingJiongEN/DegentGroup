# Project configuration
PYTHON := python3
VENV := .venv
POETRY := poetry

# Paths
SRC_DIR := teleAgent
TEST_DIR := tests
ALEMBIC := alembic

# Commands
PYTEST := $(POETRY) run pytest
UVICORN := $(POETRY) run uvicorn
MYPY := $(POETRY) run mypy
BLACK := $(POETRY) run black
ISORT := $(POETRY) run isort
FLAKE8 := $(POETRY) run flake8

.PHONY: all
all: install lint test

# Environment setup
.PHONY: install
install:
	$(POETRY) install

.PHONY: update
update:
	$(POETRY) update

# Development
.PHONY: run
run:
	$(UVICORN) main:app --reload --host 0.0.0.0 --port 8000

.PHONY: shell
shell:
	$(POETRY) shell

# Database
.PHONY: db-migrate
db-migrate:
	$(POETRY) run $(ALEMBIC) upgrade head

.PHONY: db-rollback
db-rollback:
	$(POETRY) run $(ALEMBIC) downgrade -1

.PHONY: db-revision
db-revision:
	$(POETRY) run $(ALEMBIC) revision --autogenerate -m "$(message)"

# Testing
.PHONY: test-unit
test-unit:
	$(PYTEST) $(SRC_DIR) -v --cov=$(SRC_DIR) --cov-report=term-missing -m "unit"

.PHONY: test-integration
test-integration:
	$(PYTEST) tests -v --cov=$(SRC_DIR) --cov-report=term-missing -m "integration"

.PHONY: test-agent-service
test-agent-service:
	$(PYTEST) $(SRC_DIR)/services/tests/test_agent_service.py -v --cov=$(SRC_DIR)/services/agent_service.py --cov-report=term-missing

.PHONY: test-nft
test-nft:
	$(PYTEST) $(SRC_DIR)/daos/nft/tests/test_nft_dao.py -v --cov=$(SRC_DIR)/daos/nft --cov-report=term-missing

.PHONY: test-artwork-critique
test-artwork-critique:
	$(PYTEST) $(SRC_DIR)/daos/artwork_critique/tests/test_artwork_critique_dao.py -v --cov=$(SRC_DIR)/daos/artwork_critique --cov-report=term-missing

.PHONY: test-bargaining
test-bargaining:
	$(PYTEST) $(SRC_DIR)/models/market/tests/test_bargaining.py -v --cov=$(SRC_DIR)/models/market/bargaining.py --cov-report=term-missing

.PHONY: test-artificial-market
test-artificial-market:
	$(PYTEST) $(SRC_DIR)/models/market/tests/test_artificial_market.py -v --cov=$(SRC_DIR)/models/market --cov-report=term-missing
	$(MAKE) test-bargaining

.PHONY: test
test:
	$(PYTEST) $(SRC_DIR) tests -v --cov=$(SRC_DIR) --cov-report=term-missing
	$(MAKE) test-agent-service
	$(MAKE) test-nft
	$(MAKE) test-artwork-critique
	$(MAKE) test-artificial-market

.PHONY: test-coverage
test-coverage:
	$(PYTEST) $(SRC_DIR) tests -v --cov=$(SRC_DIR) --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Code quality
.PHONY: lint
lint: format type-check style

.PHONY: format
format:
	$(BLACK) $(SRC_DIR)
	$(ISORT) $(SRC_DIR)

.PHONY: type-check
type-check:
	$(MYPY) $(SRC_DIR)

.PHONY: style
style:
	$(FLAKE8) $(SRC_DIR)

# Cleaning
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".coverage*" -exec rm -rf {} +

# Docker
.PHONY: docker-build
docker-build:
	docker build -t teleAgent:latest .

.PHONY: docker-run
docker-run:
	docker run -p 8000:8000 --env-file .env teleAgent:latest

.PHONY: dc-up
dc-up:
	docker compose up -d --build

.PHONY: dc-down
dc-down:
	docker compose down

# Help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  install        Install project dependencies"
	@echo "  update        Update project dependencies"
	@echo "  run           Run development server"
	@echo "  shell         Enter poetry shell"
	@echo "  test          Run all tests with coverage"
	@echo "  test-unit     Run unit tests"
	@echo "  test-integration  Run integration tests"
	@echo "  test-agent-service  Run agent service tests"
	@echo "  test-artwork-critique  Run artwork critique tests"
	@echo "  test-coverage      Run tests and generate HTML coverage report"
	@echo "  lint          Run all linting checks"
	@echo "  format        Format code with black and isort"
	@echo "  type-check    Run mypy type checking"
	@echo "  style         Run flake8 style checking"
	@echo "  clean         Clean up cache and build files"
	@echo "  db-migrate    Run database migrations"
	@echo "  db-rollback   Rollback last database migration"
	@echo "  db-revision   Create new database migration"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-run    Run Docker container"