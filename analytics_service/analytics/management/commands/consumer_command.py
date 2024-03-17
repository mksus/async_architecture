from kafka import KafkaConsumer
import json
from django.core.management import BaseCommand
from django.conf import settings
from django.db import DatabaseError, transaction
import jsonschema
import time
from analytics.models import DeadLetterLog

from event_schema_registry.schemas.billing_service import TransactionCreated, BalanceChanged, BillingTaskUpdated
from event_schema_registry.schemas.tracker_service import TaskCreated, TaskCompleted, TaskReassigned
from event_schema_registry.schemas.auth_service import AccountCreated, AccountUpdated, AccountRoleChanged

ACCOUNTS_STREAM = 'accounts_stream'
ACCOUNTS = 'accounts'

TASKS_STREAM = 'tasks_stream'
TASKS = 'tasks'

BILLING_TASKS = 'billing_tasks'

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

        consumer.subscribe(topics=[ACCOUNTS, ACCOUNTS_STREAM, TRANSACTIONS, BILLING_CYCLE, BILLING_TASKS])

        print('after subscribe')

        for message in consumer:
            try:
                value = message.value
                event_name = value.get("event_name")
                event_version = value.get("event_version")
                data = value["data"]
                print("Received message: {}".format(value))

                ### BARE MINIMUM TO MEET REQUIREMENTS

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


                ### ALL OBJECTS WITH EVENTUAL CONSYSTENCY

                if event_name == "AccountCreated":
                    jsonschema.validate(value, AccountCreated.v1)

                if event_name == "AccountUpdated":
                    jsonschema.validate(value, AccountUpdated.v1)

                if event_name == "AccountRoleChanged":
                    jsonschema.validate(value, AccountRoleChanged.v1)

                    # эти события нужны для авторизации и также для assignee задач

                if event_name == "BillingTaskUpdated":
                    jsonschema.validate(value, BillingTaskUpdated.v1)

                if event_name == "TaskCreated":
                    jsonschema.validate(value, TaskCreated.v2)

                    # get_or_create(public_id, **event_data) - чтобы можно было застримить второй раз / если пришло раньше создания

                if event_name == "TaskCompleted":
                    jsonschema.validate(value, TaskCompleted.v1)

                    # get_or_create(public_id, **event_data) - если оно пришло раньше создания

                if event_name == "TaskReassigned":
                    jsonschema.validate(value, TaskReassigned.v1)

                    # get_or_create(public_id, **event_data)

                    # эти события должны собирать данные о задаче из разных сервисов
                    # поддерживать eventual_consistency
                    # по ним можно будет собирать больше данных о задаче, которая осказалась самой дорогой

            except Exception as e:
                print(e)
                # запись в табличку, которую можно попробовать разгрести позже


                def is_error_retryable(e):
                    # some errors classification
                    return False

                DeadLetterLog.objects.create(
                  error=e,
                  event =message.value,
                  is_retryable=is_error_retryable(e),
                )

                # после обработать автоматом те, которые можно попробовать заретраить
                # кинуть alert по тем, которые нельзя ретраить