.PHONY: install run clean build-exe build-web lint format help

MAIN ?= main.py

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies with Poetry
	poetry install

run: ## Run the game (MAIN=main.py by default)
	poetry run python $(MAIN)

clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ __pycache__ .pytest_cache *.spec

build-exe: ## Build standalone executable with PyInstaller
	poetry run pyinstaller --onefile --windowed $(MAIN)

build-web: ## Build for web/WASM with pygbag
	poetry run pygbag $(MAIN)

lint: ## Run ruff linter
	poetry run ruff check .

format: ## Format code with ruff
	poetry run ruff format .

shell: ## Open a shell inside the Poetry venv
	poetry shell
