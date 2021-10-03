import os

from celery import Celery, app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-task-deadline-60-seconds': {
        'task': 'todo.tasks.check_tasks_deadline',
        'schedule': 60.0
    },
}
app.conf.timezone = 'UTC'
