from django.apps import AppConfig


class VidcompressbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vidcompressbot'

    def ready(self) -> None:
        import vidcompressbot.signals