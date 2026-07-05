install:
	pip install -r requirements.txt

run:
	uvicorn src.main:app --reload

test:
	pytest --cov=src --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

docker-build:
	docker build -t tickethub .