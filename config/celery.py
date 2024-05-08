import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FIXMASTER.settings')

app = Celery('FIXMASTER')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-business-status': {
        'task': 'api.tasks.update_business_status',
        'schedule': 60.0,
    },
}
