from celery import shared_task
from django.utils import timezone

from .models import Task


@shared_task
def notify_owner(task_id):
    task = Task.objects.get(pk=task_id)
    task.notify_deadline()


@shared_task
def check_tasks_deadline():
    one_h = timezone.now() + timezone.timedelta(hours=1)
    tasks = Task.objects.filter(deadline__lte=one_h, notified=False).all()
    for task in tasks:
        notify_owner.delay(task.id)
