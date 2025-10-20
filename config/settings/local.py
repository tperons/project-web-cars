from config.settings.base import *  # noqa: F401, F403
from config.settings.base import INSTALLED_APPS, MIDDLEWARE, env

DEBUG = True

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='bUhtiWJOnPD7d3VHxsneMtG08SWip0K4YVndcdgIaMXb3pFGWMfAFxXJUQJJk6K1',
)

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
    },
}


INSTALLED_APPS = ['whitenoise.runserver_nostatic', *INSTALLED_APPS]


INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', '192.168.65.1']


if env('USE_DOCKER') == 'yes':
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += ['.'.join([*ip.split('.')[:-1], '1']) for ip in ips]


INSTALLED_APPS += ['django_extensions']
