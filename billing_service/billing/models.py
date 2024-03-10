from django.db import models
from auth_client.models import User
from uuid import uuid4
from djchoices import ChoiceItem, DjangoChoices

# Create your models here.


class BillingCycle(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateTimeField(null=True, db_index=True)
    end_date = models.DateTimeField(null=True, db_index=True)
    is_active = models.BooleanField(default=False)  # управление при создании нового цикла


class Transaction(models.Model):

    # если бы были переводы между юзерами, можно было бы сделать from-to
    # но у нас либо payout юзеру, либо начисление/списание при взаимодействии с компанией
    # поэтому обойдемся типом транзакции, по которому можно будет сделать нужную аналитику
    class Type(DjangoChoices):
        payout = ChoiceItem('payout')
        company = ChoiceItem('company')

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    description = models.CharField(max_length=500, null=True)
    credit = models.PositiveIntegerField(default=0)
    debit = models.PositiveIntegerField(default=0)
    billing_cycle = models.ForeignKey(to=BillingCycle, on_delete=models.PROTECT)
    type = models.CharField(choices=Type.choices, max_length=128)


class Task(models.Model):
    class Status(DjangoChoices):
        open = ChoiceItem('open')
        complete = ChoiceItem('complete')

    id = models.BigAutoField(primary_key=True)
    public_id = models.UUIDField(unique=True, default=uuid4)
    description = models.CharField(max_length=500, null=True)
    assignee = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True)
    fee = models.PositiveIntegerField(default=0)  # при создании, kafka consumer
    reward = models.PositiveIntegerField(default=0)  # при создании, kafka consumer
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.open)