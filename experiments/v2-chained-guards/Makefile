---


## experiments/v2-chained-guards/Makefile


```makefile
# Makefile for v2 — Chained Guards


VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip


install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt


run:
	$(PYTHON) -m core.app


benchmark:
	$(PYTHON) runner/run_benchmark.py


test:
	$(PYTHON) -m pytest tests/ -v


clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +


.PHONY: install run benchmark test clean