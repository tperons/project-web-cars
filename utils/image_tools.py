import os
import uuid
from io import BytesIO

from django.core.files.base import ContentFile, File
from django.db import models
from django.utils.text import slugify
from PIL import Image


def slugify_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    slugified_name = f'{slugify(name)}{ext.lower()}'
    return slugified_name


def generate_upload_path(instance: models.Model, filename: str, base_path: str, name_attribute: str, prefix: str = '') -> str:
    extension = os.path.splitext(filename)[1]
    unique_id = uuid.uuid4().hex[:4]
    name_obj = instance
    try:
        for part in name_attribute.split('.'):
            name_obj = getattr(name_obj, part)
        base_name = str(name_obj)
    except (AttributeError, TypeError):
        base_name = 'unknown'
    slugified_name = slugify(base_name)
    return f'{base_path}/{slugified_name}/{prefix}{unique_id}{extension}'


def favicon_upload_path(instance, filename):
    return generate_upload_path(instance, filename, base_path='setup', name_attribute='title', prefix='favicon-')


def logo_upload_path(instance, filename):
    return generate_upload_path(instance, filename, base_path='setup', name_attribute='title', prefix='logo-')


def banner_upload_path(instance, filename):
    return generate_upload_path(instance, filename, base_path='setup', name_attribute='title', prefix='banner-')


def unknown_car_upload_path(instance, filename):
    return generate_upload_path(instance, filename, base_path='setup', name_attribute='title', prefix='unknown-')


def cover_upload_path(instance, filename):
    return generate_upload_path(instance, filename, base_path='cars', name_attribute='model', prefix='cover-')


def photo_upload_path(instance, filename):
    return generate_upload_path(instance, filename, base_path='cars', name_attribute='car.model', prefix='photo-')


def resize_and_pad(image_django: File, aspect_width: int, aspect_height: int, target_width: int, background_color: str = 'black', optimize: bool = True, quality: int = 75) -> ContentFile:
    image_content = image_django.read()
    image_pillow = Image.open(BytesIO(image_content))

    original_width, original_height = image_pillow.size
    original_ratio = original_width / original_height

    target_height = int(target_width * aspect_height / aspect_width)
    canvas_size = (target_width, target_height)
    canvas_ratio = target_width / target_height

    if original_ratio > canvas_ratio:
        new_width = target_width
        new_height = int(new_width / original_ratio)
    else:
        new_height = target_height
        new_width = int(new_height * original_ratio)

    resized_image = image_pillow.resize((new_width, new_height), Image.Resampling.LANCZOS)

    new_canvas = Image.new(image_pillow.mode, canvas_size, background_color)

    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    paste_position = (paste_x, paste_y)

    new_canvas.paste(resized_image, paste_position)

    buffer = BytesIO()
    if new_canvas.mode in ('RGBA', 'P'):
        new_canvas = new_canvas.convert('RGB')
    new_canvas.save(buffer, format='JPEG', optimize=optimize, quality=quality)

    return ContentFile(buffer.getvalue(), name=image_django.name)


def convert_image(image_django: File, target_format: str = 'WEBP', optimize: bool = True, quality: int = 75) -> ContentFile:
    image_content = image_django.read()
    image_pillow = Image.open(BytesIO(image_content))

    buffer = BytesIO()

    if image_pillow.mode in ('RGBA', 'P'):
        image_pillow = image_pillow.convert('RGB')

    image_pillow.save(buffer, format=target_format.upper(), optimize=optimize, quality=quality)

    original_name_without_ext = os.path.splitext(image_django.name)[0]
    new_filename = f'{original_name_without_ext}.{target_format.lower()}'

    return ContentFile(buffer.getvalue(), name=new_filename)
