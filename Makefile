.PHONY: lint run clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  lint    - Auto-fix linting issues and format code"
	@echo "  run     - Run the main.py file"
	@echo "  clean   - Remove cache files"
	@echo "  help    - Show this help message"

# Auto-fix linting issues and format
lint:
	uv run ruff check --fix .
	uv run ruff format .

# Run the main application
run:
	uv run python main.py

# Clean cache files
clean:
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete