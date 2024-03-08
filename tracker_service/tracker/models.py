from django.contrib.auth.models import AbstractUser
from django.db import models
from auth_client.models import User
from djchoices import ChoiceItem, DjangoChoices
import random


class Task(models.Model):

    class Status(DjangoChoices):
        open = ChoiceItem('open')
        complete = ChoiceItem('complete')

    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=500, null=True)
    assignee = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True)
    fee = models.PositiveIntegerField(default=0)
    reward = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.open)


def create_new_task(description=None):
    fee = random.randint(10, 20)
    reward = random.randint(20, 40)
    # assignee = User.objects.get(id=1)  # todo поменять на рандомного
    new_task = Task.objects.create(description=description, fee=fee, reward=reward)
    new_task.save()


def reassign_tasks():
    open_tasks = Task.objects.filter(status=Task.Status.open)
    for task in open_tasks:
        print(f'call assign task {task.id}')


def complete_task(task_id, user_id):
    task = Task.objects.get(id=task_id)  # тут может упасть, если такси нет
    if not task.assignee_id or task.assignee_id != user_id:
        raise 'wrong user'
    task.status = Task.Status.complete
    task.save()
