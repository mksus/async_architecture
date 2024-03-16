from kafka import KafkaConsumer
import json
from django.core.management import BaseCommand
from django.conf import settings

ACCOUNTS_STREAM = 'accounts_stream'
ACCOUNTS = 'accounts'

TASKS_STREAM = 'tasks_stream'
TASKS = 'tasks'


class Command(BaseCommand):
    help = "Start Reporting Kafka Consumer"

    def handle(self, *args, **kwargs):

        print(settings.KAFKA_BROKER)

        consumer = KafkaConsumer(
            bootstrap_servers=[settings.KAFKA_BROKER],
            group_id='async_arc',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            api_version=(2, 0)
        )

        consumer.subscribe(topics=[ACCOUNTS, ACCOUNTS_STREAM, TASKS_STREAM, TASKS])

        print('after subscribe')

        for message in consumer:
            value = message.value

            #  по-хорошему, любые манипуляции с полями должны быть под try-except,
            #  пока не хватает сил/времени на переделку, считаем, что все события их содержат

            event_name = value.get("event_name")
            event_version = value.get("event_version")
            data = value["data"]
            print("Received message: {}".format(value))

