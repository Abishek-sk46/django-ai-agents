import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neurocore.settings")

app = Celery("neurocore")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

