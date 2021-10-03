from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Task(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    notified = models.BooleanField(default=False)

    def notify_deadline(self):
        if self.owner.email:
            deadline = self.deadline.strftime("%Y-%m-%d %H:%M")
            send_mail(
                f'Deadline notification for task "{self.title}"',
                f'The deadline for the task "{self.title}" comes at {deadline}',
                'info@todo-site.com',
                [self.owner.email]
            )

        self.notified = True
        self.save()
