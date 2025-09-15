import logging
import os
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



