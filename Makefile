flake8-check:
	flake8 --config=.flake8

up_compose:
	docker compose -f docker-compose.yml up -d
down_compose:
	docker compose -f docker-compose.yml down