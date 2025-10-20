from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView

from apps.cars.models import Car, CarInventory
from apps.users.forms import CustomAuthenticationForm, CustomUserCreationForm
from apps.users.mixins import LoggedOutOnlyMixin


class RegisterView(LoggedOutOnlyMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/pages/user_register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    success_message = "Registo realizado com sucesso! A sua conta aguarda aprovação de um administrador."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Crie a sua conta.',
            'register_form': context['form'],
        })
        return context


class CustomLoginView(LoggedOutOnlyMixin, LoginView):
    template_name = 'users/pages/user_login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Login realizado com sucesso. Bem-vindo(a) de volta!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Acesse a sua Conta',
            'login_form': context['form'],
        })
        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/pages/user_dashboard.html'
    login_url = reverse_lazy('users:login')

    def _get_inventory_summary(self):
        return CarInventory.objects.first()

    def _get_cars_in_stock(self):
        return (
            Car.objects
            .select_related('brand', 'owner')
            .prefetch_related('optionals', 'image')
            .order_by('status', '-pk')
        )

    def _get_recent_sales_stats(self):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        stats = Car.objects.filter(
            status=Car.Status.SOLD,
            sold_at__gte=thirty_days_ago
        ).aggregate(
            count=Count('id'),
            total_value=Sum('value')
        )
        return {
            'count': stats.get('count', 0),
            'value': stats.get('total_value', 0) or 0
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_sales = self._get_recent_sales_stats()
        context.update({
            'title': 'Dashboard',
            'cars_inventory': self._get_inventory_summary(),
            'cars_stock': self._get_cars_in_stock(),
            'recent_sales_count': recent_sales['count'],
            'recent_sales_value': recent_sales['value'],
        })
        return context
