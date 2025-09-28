# Makefile for v1 — Simple Filters & Scoped Prompts

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Install dependencies
install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run the app
run:
	$(PYTHON) -m core.app

# Run tests
test:
	$(PYTHON) -m pytest tests/ -v

# Lint with flake8 (or black if configured)
lint:
	$(PYTHON) -m flake8 core tests

# Format with black
format:
	$(PYTHON) -m black core tests

# Clean up virtual environment
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: install run test lint format clean