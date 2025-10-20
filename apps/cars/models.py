from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.image_tools import cover_upload_path, photo_upload_path


class Brand(models.Model):
    name = models.CharField(verbose_name='Marca')

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Optional(models.Model):
    name = models.CharField(verbose_name='Opcional', max_length=64)

    class Meta:
        verbose_name = 'Opcional'
        verbose_name_plural = 'Opcionais'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Car(models.Model):

    class Status(models.TextChoices):
        SOLD = 'SOLD', _('Vendido')
        AVAILABLE = 'AVAILABLE', _('Disponível')
        OLD_STOCK = 'OLD_STOCK', _('Estoque Antigo')

    class Transmission(models.TextChoices):
        AT = 'AT', _('Automática')
        MT = 'MT', _('Manual')
        CVT = 'CVT', _('CVT')

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='car_brand', verbose_name='Marca')
    model = models.CharField(verbose_name='Modelo', max_length=64)
    year = models.IntegerField(verbose_name='Ano')
    version = models.CharField(verbose_name='Versão', max_length=64)
    value = models.FloatField(verbose_name='Valor')
    ai_description = models.BooleanField(verbose_name='Descrição Automática', default=False)
    description = models.TextField(verbose_name='Descrição', blank=True)
    mileage = models.IntegerField(verbose_name='Quilometragem')
    transmission = models.CharField(verbose_name='Transmissão', max_length=16, choices=Transmission.choices)
    color = models.CharField(verbose_name='Cor')
    cover = models.ImageField(verbose_name='Capa', upload_to=cover_upload_path, blank=True, null=True)
    optionals = models.ManyToManyField(Optional, related_name='car_optional', verbose_name='Opcionais', blank=True)
    created_at = models.DateTimeField(verbose_name='Data de Entrada', auto_now_add=True)
    status = models.CharField(verbose_name='Status', max_length=16, default=Status.AVAILABLE, choices=Status.choices)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Responsável', blank=True, null=True)
    sold_at = models.DateTimeField(verbose_name='Vendido em', blank=True, null=True)

    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'

    @property
    def days_in_stock(self):
        if not self.created_at:
            return 0
        start_date = self.created_at.date()
        if self.sold_at:
            end_date = self.sold_at.date()
        else:
            end_date = timezone.now().date()
        delta = end_date - start_date
        return max(0, delta.days)

    def __str__(self):
        return f'{self.brand} {self.model} {self.year}'


class CarImages(models.Model):
    front_view = models.ImageField(verbose_name='Visão frontal', upload_to=photo_upload_path, blank=True, null=True)
    side_view = models.ImageField(verbose_name='Visão lateral', upload_to=photo_upload_path, blank=True, null=True)
    back_view = models.ImageField(verbose_name='Visão traseira', upload_to=photo_upload_path, blank=True, null=True)
    interior_view = models.ImageField(verbose_name='Visão interior', upload_to=photo_upload_path, blank=True, null=True)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='image')

    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'

    def __str__(self):
        return f'Imagens do(a) {self.car.model}'


class CarInventory(models.Model):
    cars_count = models.IntegerField(verbose_name='Quantidade de carros')
    cars_value = models.FloatField(verbose_name='Valor total dos carros')
    created_at = models.DateTimeField(verbose_name='Data da contagem', auto_now_add=True)

    class Meta:
        verbose_name = 'Inventário'
        verbose_name_plural = 'Inventários'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.cars_count} - {self.cars_value}'
        return f'{self.cars_count} - {self.cars_value}'
