COMPOSE_PROJECT_NAME_DEV=test_task_dev

COMPOSE_FILE_DEV = docker/docker-compose.dev.yaml
ENV_FILE = .env

DC_DEV=docker compose -f $(COMPOSE_FILE_DEV) -p $(COMPOSE_PROJECT_NAME_DEV) --env-file $(ENV_FILE)

.PHONY: help \
build up down stop restart logs shell \
startapp makemigrations migrate superuser static 


# ====================================================================================

build:
	$(DC_DEV) build

up:
	$(DC_DEV) up -d

down:
	$(DC_DEV) down $(args)

stop:
	$(DC_DEV) stop

restart:
	$(DC_DEV) restart $(s)

logs:
	$(DC_DEV) logs -f $(s)

shell:
	$(DC_DEV) exec $(s) sh

startapp:
	$(DC_DEV) exec backend python backend/manage.py startapp $(args)

makemigrations:
	$(DC_DEV) exec backend python backend/manage.py makemigrations $(args)

migrate:
	$(DC_DEV) exec backend python backend/manage.py migrate

superuser:
	$(DC_DEV) exec backend python backend/manage.py createsuperuser

static:
	$(DC_DEV) exec backend python backend/manage.py collectstatic --noinput

