from tracker.kafka_producer import dispatch_task_created

from django.core.management import BaseCommand
from django.conf import settings

from tracker.models import Task


class Command(BaseCommand):
    help = "Stream all users to other services"

    def handle(self, *args, **kwargs):

        print(settings.KAFKA_BROKER)
        tasks = Task.objects.all()
        for t in tasks:
            print(t)
            dispatch_task_created(t)

