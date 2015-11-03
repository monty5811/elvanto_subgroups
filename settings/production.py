import os

import dj_database_url

from settings.base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'set this in heroku')
DEBUG = False
ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOST', '*')]

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'

# OPBEAT
INSTALLED_APPS += [
    "opbeat.contrib.django",
]

OPBEAT = {
    "ORGANIZATION_ID": os.environ.get('OPBEAT_ORG_ID', ''),
    "APP_ID": os.environ.get('OPBEAT_APP_ID', ''),
    "SECRET_TOKEN": os.environ.get('OPBEAT_SECRET_TOKEN', ''),
}

MIDDLEWARE_CLASSES = [
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'sslify.middleware.SSLifyMiddleware',
] + MIDDLEWARE_CLASSES

LOGGING = {
    "version": 1,
    # Don't throw away default loggers.
    "disable_existing_loggers": False,
    "handlers": {
        # Redefine console logger to run in production.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        # Redefine django logger to use redefined console logging.
        "django": {
            "handlers": ["console"],
        }
    }
}

# Security:
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + [
    'django.middleware.security.SecurityMiddleware',
]
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
