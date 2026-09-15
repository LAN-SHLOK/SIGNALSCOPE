.PHONY: install install-dev train evaluate test lint format docker-up docker-down clean

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

train:
	python model/train.py

evaluate:
	python model/evaluate.py

predict:
	python predict.py --image $(IMAGE)

server:
	uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm run dev

test:
	pytest tests/ -v --tb=short

lint:
	ruff check src/ api/ app/ scripts/ tests/

format:
	black src/ api/ app/ scripts/ tests/

docker-up:
	docker compose up --build

docker-down:
	docker compose down

download-weights:
	python -c "import torch; torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14')"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf outputs/logs/* outputs/predictions/* outputs/heatmaps/*
