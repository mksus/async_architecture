# Generated by Django 5.0.2 on 2024-03-10 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_task_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='fee',
        ),
        migrations.RemoveField(
            model_name='task',
            name='reward',
        ),
    ]