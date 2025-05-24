.PHONY: setup install clean run

VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

setup: check-uv create-venv

check-uv:
	@which uv >/dev/null 2>&1 || (echo "Installing uv..." && curl -LsSf https://astral.sh/uv/install.sh | sh)

create-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..." && \
		uv venv $(VENV_DIR); \
	fi

install: setup
	@echo "Installing dependencies..."
	@uv sync

run: install
	@echo "Starting FastAPI production server..."
	@$(VENV_DIR)/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV_DIR)
