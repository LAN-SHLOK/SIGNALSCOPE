.PHONY: install install-dev train evaluate test lint format docker-up docker-down clean

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

train:
	python scripts/train.py

evaluate:
	python scripts/evaluate.py

predict:
	python src/model/predict.py --image $(IMAGE)

app:
	streamlit run app/streamlit_app.py

test:
	pytest tests/ -v --tb=short

lint:
	ruff check src/ app/ scripts/ tests/

format:
	black src/ app/ scripts/ tests/

docker-up:
	docker compose -f docker/docker-compose.yml up --build

docker-down:
	docker compose -f docker/docker-compose.yml down

download-weights:
	python scripts/download_weights.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf outputs/logs/* outputs/predictions/* outputs/heatmaps/*
