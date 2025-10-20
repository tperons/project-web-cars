from django.apps import AppConfig


class SiteSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.site_setup'
    verbose_name = 'Site Setup'

    def ready(self):
        from . import signals  # noqa: F401
