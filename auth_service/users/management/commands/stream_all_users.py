from users.kafka_producer import dispatch_account_updated

from django.core.management import BaseCommand
from django.conf import settings

from users.models import User


class Command(BaseCommand):
    help = "Stream all users to other services"

    def handle(self, *args, **kwargs):

        print(settings.KAFKA_BROKER)
        users = User.objects.all()
        for u in users:
            print(u)
            dispatch_account_updated(u)


