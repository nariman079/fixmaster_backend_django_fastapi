"""
Celery in project
"""

import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("django_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "update-bookings-gauge": {
        "task": "src.tasks.csm_metrics_tasks.update_metrics",  # путь к твоей задаче
        "schedule": 10.0,  # каждые 10 секунд
    },
}
