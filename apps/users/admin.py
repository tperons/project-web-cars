from django.contrib import admin
from django.contrib.auth.models import User


class CustomUserAdmin(admin.ModelAdmin):
    actions = ('approve_users',)
    list_display = ('first_name', 'username', 'is_active', 'is_staff',)
    list_editable = ('is_active', 'is_staff',)
    ordering = ('pk',)

    @admin.action(description='Aprovar Usuário(s)')
    def approve_users(self, request, queryset):
        rows_updated = queryset.update(is_active=True)
        if rows_updated == 1:
            message = "1 usuário foi aprovado com sucesso."
        else:
            message = f"{rows_updated} usuários foram aprovados com sucesso."
        self.message_user(request, message)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
