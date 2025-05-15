.PHONY: test
test:
	pytest

.PHONY: lint
lint:
	flake8 .

.PHONY: format
format:
	black .

.PHONY: check
check: lint test

.PHONY: install
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

.PHONY: clean
clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
