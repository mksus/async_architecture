from kafka import KafkaConsumer
import json
from django.core.management import BaseCommand
from django.conf import settings
from django.db import DatabaseError, transaction
import jsonschema
import time

from event_schema_registry.schemas.billing_service import TransactionCreated, BalanceChanged

ACCOUNTS_STREAM = 'accounts_stream'
ACCOUNTS = 'accounts'

TASKS_STREAM = 'tasks_stream'
TASKS = 'tasks'

TRANSACTIONS = 'transactions'
BILLING_CYCLE = 'billing_cycle'


class Command(BaseCommand):
    help = "Start Reporting Kafka Consumer"

    def handle(self, *args, **kwargs):

        print(settings.KAFKA_BROKER)
        print('steeping 10 sec')
        time.sleep(10)

        consumer = KafkaConsumer(
            bootstrap_servers=[settings.KAFKA_BROKER],
            group_id='analytice_service',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            api_version=(2, 0)
        )

        consumer.subscribe(topics=[ACCOUNTS, ACCOUNTS_STREAM, TRANSACTIONS, BILLING_CYCLE])

        print('after subscribe')

        for message in consumer:
            try:
                value = message.value
                event_name = value.get("event_name")
                event_version = value.get("event_version")
                data = value["data"]
                print("Received message: {}".format(value))

                if event_name == "TransactionCreated":
                    jsonschema.validate(value, TransactionCreated.v1)
                    with transaction.atomic():
                        print('handle transaction created')
                        transaction_type = value.get("type")
                        debit = value.get("debit")
                        credit = value.get("credit")
                        if transaction_type == 'company':
                            if debit:
                                print("Апдейтим дашборд с самыми дорогими задачами, потому что сейчас других credit-ов нет")
                                pass
                            if credit:
                                print("Апдейтим дашборд сколько заработал топ-менеджмент")
                                pass

                if event_name == "BalanceChanged":
                    jsonschema.validate(value, BalanceChanged.v1)
                    with transaction.atomic():
                        print('handle Balance changed')
                        billing_cycle_start_date = value.get("billing_cycle_start_date")
                        balance = value.get("balance")
                        username = value.get("username")

                        # обновить статистики про отрицателдьные балансы в определенный billing cycle
                        print("NegativeBalances.update_by_username(username, balance, billing_cycle_start_date)")

            except Exception as e:
                print(e)