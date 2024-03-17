from django.core.management import BaseCommand
from django.db import DatabaseError, transaction
from datetime import datetime
from billing.kafka_producer import
from billing.models import BillingCycle


class Command(BaseCommand):
    help = "Start Reporting Kafka Consumer"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            try:
                current_cycle = BillingCycle.objects.get(is_active=True)
                current_cycle.end_date = datetime.now()
                current_cycle.is_active = False
                current_cycle.save()
            except BillingCycle.DoesNotExist as e:
                print('no previous cycle')


            new_cycle = BillingCycle.objects.create(start_date=datetime.now(), is_active=True)
            print(new_cycle)







