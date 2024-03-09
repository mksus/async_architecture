from django.contrib.auth.models import AbstractUser
from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.kafka_producer import dispatch_account_changed, dispatch_account_created, dispatch_role_changed


class User(AbstractUser):

    class Role(DjangoChoices):
        admin = ChoiceItem('admin')
        manager = ChoiceItem('manager')
        accountant = ChoiceItem('accountant')
        dev = ChoiceItem('dev')

    role = models.CharField(choices=Role.choices, max_length=128, default=Role.dev)
    email = models.EmailField()

    #  AbstractUser.username is public_id because django-oauth-toolkit uses it in /introspect request
    #  so auth binds users by username in other services


# method for updating
@receiver(pre_save, sender=User)
def update_stock(sender, instance, **kwargs):
    event_data = None
    created = instance.id is None
    if created:
        dispatch_account_created(instance)
    else:
        previous = User.objects.get(id=instance.id)
        if previous.role != instance.role:
            print('role_changed')
            dispatch_role_changed(instance)
        dispatch_account_changed(instance)


