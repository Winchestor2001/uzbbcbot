# Makefile для управления проектом uzbbcbot

# Переменные
COMPOSE=docker-compose
PROJECT_NAME=uzbbcbot
DJANGO_CONTAINER=django_drf
BOT_CONTAINER=tg_bot

# Команды Docker Compose
up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down && $(COMPOSE) up -d

run:
	$(COMPOSE) down && $(COMPOSE) up --build -d

logs:
	$(COMPOSE) logs -f

logs-web:
	$(COMPOSE) logs -f web

logs-bot:
	$(COMPOSE) logs -f bot

# Django команды
migrate:
	$(COMPOSE) exec $(DJANGO_CONTAINER) python manage.py migrate

makemigrations:
	$(COMPOSE) exec $(DJANGO_CONTAINER) python manage.py makemigrations

createsuperuser:
	$(COMPOSE) exec $(DJANGO_CONTAINER) python manage.py createsuperuser

shell:
	$(COMPOSE) exec $(DJANGO_CONTAINER) python manage.py shell

collectstatic:
	$(COMPOSE) exec $(DJANGO_CONTAINER) python manage.py collectstatic --noinput

# Очистка
prune:
	docker system prune -af --volumes

# Перезапуск бота
restart-bot:
	$(COMPOSE) restart $(BOT_CONTAINER)
