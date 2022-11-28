import logging
import os

from celery import Celery

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.develop")

app = Celery("InstaShare-API")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

logger.debug(f"Celery conf: {app.conf}")
