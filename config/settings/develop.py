"""
This is the settings file that you use when you're working on the project locally.
Local development-specific include DEBUG mode, log level, and activation of developer tools like django-debug-toolsbar
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "qov#ce&bl3z8@ymehv1byt^beru%el-0wjo%e#1q8#og6331ik"

ALLOWED_HOSTS = ["*"]

# email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {"handlers": ["console"], "level": "WARNING"},
        "apps.files": {"handlers": ["console"], "level": "INFO"},
        "apps.core": {"handlers": ["console"], "level": "INFO"},
        "config": {"handlers": ["console"], "level": "DEBUG"},
    },
}

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
