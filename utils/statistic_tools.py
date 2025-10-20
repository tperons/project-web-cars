from django.db import transaction
from django.db.models import Sum

from apps.cars.models import Car, CarInventory


@transaction.atomic
def car_inventory_update() -> None:
    cars_in_stock = Car.objects.exclude(status=Car.Status.SOLD)
    cars_count = cars_in_stock.count()
    cars_value_aggregation = cars_in_stock.aggregate(total_value=Sum('value'))
    cars_value = cars_value_aggregation['total_value'] or 0
    CarInventory.objects.update_or_create(pk=1, defaults={'cars_count': cars_count, 'cars_value': cars_value})
