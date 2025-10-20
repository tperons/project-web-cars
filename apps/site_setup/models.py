from django.db import models

from utils.image_tools import (
    banner_upload_path,
    favicon_upload_path,
    logo_upload_path,
    unknown_car_upload_path,
)


class Setup(models.Model):
    title = models.CharField(verbose_name='Título', max_length=32)
    description = models.TextField(verbose_name='Descrição do Site', blank=True, help_text='Descrição curta do site para SEO')
    favicon = models.ImageField(verbose_name='Favicon', upload_to=favicon_upload_path, blank=True, null=True)
    logo = models.ImageField(verbose_name='Logo', upload_to=logo_upload_path, blank=True, null=True)
    banner = models.ImageField(verbose_name='Banner', upload_to=banner_upload_path, blank=True, null=True)
    unknown_car = models.ImageField(verbose_name='Carro Desconhecido', upload_to=unknown_car_upload_path, blank=True, null=True)

    header_title = models.CharField(verbose_name='Título do header princial', max_length=128, blank=True, help_text='O título principal exibido na página inicial.')
    header_subtitle = models.TextField(verbose_name='Subtítulo do Header', blank=True, help_text='O texto de apoio exibido abaixo do título principal.')

    address = models.CharField(verbose_name='Endereço', max_length=256, blank=True)
    email = models.EmailField(verbose_name='Email de Contato', blank=True)
    phone_number = models.CharField(verbose_name='Número de Telefone', max_length=13, blank=True, help_text='Ex: 5562912345678 (Código do País + Código de Área + Número)')
    whatsapp_number = models.CharField(verbose_name='Número do Whatsapp', max_length=13, blank=True, help_text='Ex: 5562912345678 (Código do País + Código de Área + Número)')

    facebook_url = models.URLField(verbose_name='Link do Facebook', blank=True)
    twitter_url = models.URLField(verbose_name='Link do X/Twitter', blank=True)
    instagram_url = models.URLField(verbose_name='Link do Instagram', blank=True)

    about = models.TextField(verbose_name='Sobre', blank=True, help_text='Texto a ser exibido no footer.')

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'

    def __str__(self):
        return self.title
