.PHONY: lint format install-dev run-web

lint:
	poetry run flake8 src

format:
	poetry run black src
	poetry run isort .

install-dev:
	poetry install

run-web:
	poetry run uvicorn nft_russian_roulette.web.app:app --reload
