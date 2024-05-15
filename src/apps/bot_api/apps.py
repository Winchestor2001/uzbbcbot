from django.apps import AppConfig


class BotApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_api'

    def ready(self):
        import bot_api.signals
