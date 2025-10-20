from django.urls import path

from apps.cars.views import (
    CarCreateView,
    CarDeleteView,
    CarDetailView,
    CarListView,
    CarSearchView,
    CarSoldView,
    CarUpdateView,
    CreateRelatedObjectView,
)

app_name = 'cars'

urlpatterns = [
    path('create/', CarCreateView.as_view(), name='car_create'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('search/', CarSearchView.as_view(), name='car_search'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/sold/', CarSoldView.as_view(), name='car_sold'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('api/create-related/', CreateRelatedObjectView.as_view(), name='api_create_related'),
]
