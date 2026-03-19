.PHONY: lint test coverage clean install help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dev dependencies
	pip install -r requirements-dev.txt

lint: ## Run ansible-lint and flake8
	ansible-lint .
	flake8 library/

test: ## Run unit tests
	pytest tests/ -v --tb=short

coverage: ## Run tests with coverage report
	pytest tests/ -v --tb=short --cov=library --cov-report=term --cov-report=html

syntax: ## Ansible playbook syntax check
	ansible-playbook pl_npm-management.yml --syntax-check

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

clean: ## Remove build artifacts
	rm -rf .pytest_cache htmlcov .coverage __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
