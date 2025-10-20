from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.cars.models import Brand, Car, Optional
from utils.gemini_tools import generate_ai_description
from utils.statistic_tools import car_inventory_update


@receiver(pre_save, sender=Brand)
def capitalize_brand_name(sender, instance, **kwargs):

    if instance.name:
        instance.name = instance.name.capitalize()


@receiver(pre_save, sender=Optional)
def capitalize_optional_name(sender, instance, **kwargs):

    if instance.name:
        instance.name = instance.name.capitalize()


@receiver(pre_save, sender=Car)
def capitalize_car_instance(sender, instance, **kwargs):

    if instance.model:
        instance.model = instance.model.capitalize()

    if instance.version:
        instance.version = instance.version.capitalize()

    if instance.color:
        instance.color = instance.color.capitalize()

    if instance.description:
        instance.description = instance.description.capitalize()


@receiver(pre_save, sender=Car)
def generate_car_description(sender, instance, **kwargs):
    if not instance.description and instance.ai_description:
        try:
            ai_description = generate_ai_description(instance.brand, instance.model, instance.version, instance.year)
            instance.description = ai_description
        except Exception as e:
            print(f"AVISO: Falha ao gerar descrição de IA para o carro a ser criado: {e}")
            instance.description = "Falha ao gerar a descrição automática. Por favor, edite manualmente."


@receiver([post_save, post_delete], sender=Car)
def update_inventory_on_change(sender, instance, **kwargs):
    car_inventory_update()
    car_inventory_update()
