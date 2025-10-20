from django.contrib import admin
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.site_setup.models import Setup


@receiver(post_migrate)
def set_admin_titles(sender, **kwargs):
    if sender.name == 'setup':
        try:
            setup = Setup.objects.filter(title__gt='').first()
            if setup:
                admin.site.site_header = 'Área Administrativa'
                admin.site.site_title = f'Portal de Administração do {setup.title}'
                admin.site.index_title = f'Bem vindo à(o) {setup.title}'
        except Exception:
            pass
