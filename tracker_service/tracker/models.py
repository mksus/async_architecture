from django.contrib.auth.models import AbstractUser
from django.db import models
from auth_client.models import User
from djchoices import ChoiceItem, DjangoChoices
from django.db.models.signals import pre_save
from django.dispatch import receiver
from tracker.kafka_producer import dispatch_task_created
from uuid import uuid4


class Task(models.Model):

    class Status(DjangoChoices):
        open = ChoiceItem('open')
        complete = ChoiceItem('complete')

    id = models.BigAutoField(primary_key=True)
    public_id = models.UUIDField(unique=True, default=uuid4)
    description = models.CharField(max_length=500, null=True)
    assignee = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.open)


# method for updating
@receiver(pre_save, sender=Task)
def task_events(sender, instance, **kwargs):
    created = instance.id is None
    if created:
        dispatch_task_created(instance)
    else:
        previous = User.objects.get(id=instance.id)
        if previous.status != Task.Status.complete and instance.status == Task.Status.complete:
            dispatch_role_changed(instance)
        dispatch_account_changed(instance)