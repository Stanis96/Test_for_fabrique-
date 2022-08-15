import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fabrique_notification_service.settings")

app = Celery("fabrique_notification_service")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
