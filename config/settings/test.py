from config.settings.base import *  # noqa: F401, F403
from config.settings.base import TEMPLATES, env

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='CrDsnDLlwGisGFh3ydLdHPgHDA8iTqtjE5GOECNuH7wxgZhmdlUEKhgqnOFGcpp1',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'


PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']


EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


TEMPLATES[0]['OPTIONS']['debug'] = True


MEDIA_URL = 'http://media.testserver/'
