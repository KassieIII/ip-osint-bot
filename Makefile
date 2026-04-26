.PHONY: install run test lint fmt docker

install:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio ruff

run:
	python -m bot.main

test:
	pytest tests/ -v

lint:
	ruff check bot/ --select E,F,W --ignore E501

fmt:
	ruff format bot/

docker:
	docker build -t ip-osint-bot .
