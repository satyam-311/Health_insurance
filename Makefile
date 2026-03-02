.PHONY: install run train test lint format docker-build docker-run

install:
	pip install -r requirements.txt

run:
	uvicorn src.api.main:app --reload

train:
	python -m src.models.train

test:
	pytest -q

lint:
	flake8 src tests

format:
	black src tests

docker-build:
	docker build -t health-insurance-api .

docker-run:
	docker compose up --build
