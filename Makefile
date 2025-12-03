up:
	docker compose -f docker-compose.yml up

test:
	docker compose -f docker-compose.test.yml run --rm backend pytest

linter:
	docker compose -f docker-compose.yml run --rm backend poetry run ruff check . --statistics

createsuperuser:
	docker compose -f docker-compose.yml run --rm backend poetry run python manage.py create_admin --username $(USERNAME) --password $(PASSWORD)
