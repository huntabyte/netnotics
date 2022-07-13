.PHONY: revision migrate


revision:
	docker compose exec backend alembic revision --autogenerate -m 'message'

migrate:
	docker compose exec backend alembic upgrade head

backend-logs:
	docker compose logs -f backend

psql:
	docker compose exec postgres psql -U postgres
