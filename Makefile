dev:
	docker compose up --build

prod:
	docker compose --env-file .env.prod up --build -d

down:
	docker compose down --remove-orphans

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps
