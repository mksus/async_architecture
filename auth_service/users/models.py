from django.contrib.auth.models import AbstractUser
from django.db import models
from djchoices import ChoiceItem, DjangoChoices


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