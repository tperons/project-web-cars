from django.contrib import admin

from apps.site_setup.forms import SetupModelForm
from apps.site_setup.models import Setup


@admin.register(Setup)
class SetupAdmin(admin.ModelAdmin):
    form = SetupModelForm
    list_display = ('title', 'has_favicon', 'has_logo', 'has_banner')

    def has_add_permission(self, request):
        return not Setup.objects.exists()

    def has_favicon(self, object):
        return bool(object.favicon)
    has_favicon.boolean = True

    def has_logo(self, object):
        return bool(object.logo)
    has_logo.boolean = True

    def has_banner(self, object):
        return bool(object.banner)
    has_banner.boolean = True
