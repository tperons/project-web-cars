from pathlib import Path

import environ
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / 'apps'
env = environ.Env()


READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / '.env'))


DEBUG = env.bool('DJANGO_DEBUG', False)
TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True


DATABASES = {'default': env.db('DATABASE_URL')}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
]
THIRD_PARTY_APPS = [
]
LOCAL_APPS = [
    'apps.cars',
    'apps.site_setup',
    'apps.users',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(APPS_DIR / 'static')]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


MEDIA_ROOT = str(APPS_DIR / 'media')
MEDIA_URL = '/media/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.setup_context_processor',
            ],
        },
    },
]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'


FIXTURE_DIRS = (str(APPS_DIR / 'fixtures'),)


SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'


ADMIN_URL = 'admin/'
ADMINS = [
    ('Tiago Perons', 'tperons@gmail.com'),
]
MANAGERS = ADMINS
DJANGO_ADMIN_FORCE_ALLAUTH = env.bool('DJANGO_ADMIN_FORCE_ALLAUTH', default=False)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(message)s'},
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {'level': 'INFO', 'handlers': ['console']},
}


REDIS_URL = env('REDIS_URL', default='redis://redis:6379/0')
REDIS_SSL = REDIS_URL.startswith('rediss://')

LOGIN_REDIRECT_URL = reverse_lazy('users:dashboard')
LOGIN_URL = reverse_lazy('users:login')
LOGOUT_REDIRECT_URL = reverse_lazy('index')
