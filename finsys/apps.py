from django.apps import AppConfig


class FinsysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finsys'

    def ready(self):
        import finsys.signals
