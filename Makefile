dev:
	docker compose -f docker-compose-dev.yaml --env-file .env-dev up --build

prod:
	docker compose -f docker-compose-prod.yaml --env-file .env-prod up --build

test:
	docker compose -f docker-compose-test.yaml --env-file .env-test up --build
