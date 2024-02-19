from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE

INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE