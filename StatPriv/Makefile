install:
	@echo ">>> Installing dependencies"
	pip install --upgrade pip
	pip install -r requirements.txt

format: 
	@echo ">>> Formating files with isort and Black"
	isort .
	black .

lint:
	@echo ">>> Linting Python files"
	ruff check .

test: 
	@echo ">>> Running unit tests"
	python -m pytest -vv
