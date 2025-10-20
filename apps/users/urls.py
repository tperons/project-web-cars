from django.urls import path

from apps.users.views import (
    CustomLoginView,
    CustomLogoutView,
    DashboardView,
    RegisterView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
