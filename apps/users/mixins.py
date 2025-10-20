from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoggedOutOnlyMixin:
    redirect_url = reverse_lazy('users:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
