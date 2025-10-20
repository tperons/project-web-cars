from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cars'
    verbose_name = 'Carros'

    def ready(self):
        from apps.cars import signals  # noqa: F401
