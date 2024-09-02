from django.apps import AppConfig


class FirstGameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'first_game'

    def ready(self) -> None:
        import first_game.signals