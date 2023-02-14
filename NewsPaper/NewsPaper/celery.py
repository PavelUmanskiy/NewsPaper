import os
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
 
app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()