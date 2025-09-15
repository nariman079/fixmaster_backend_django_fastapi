import logging
import socket
import os
from django.core.signals import request_started
from django.dispatch import receiver
from django.apps import AppConfig


logger = logging.getLogger('src.system')

class SrcAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src"
    verbose_name = "СУБ"

   

    def shutdown(self):
        logger.info("Приложение остановлено", extra={
            'event': 'system.app.stopped',
            'pid': os.getpid()
        })



