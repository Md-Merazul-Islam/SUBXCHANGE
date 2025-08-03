from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import multiprocessing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

multiprocessing.set_start_method('spawn', force=True)

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery."""
    print(f'Request: {self.request!r}')