from kafka import KafkaConsumer
import json
from auth_client.models import User
from billing.models import Task, Transaction

from event_schema_registry.schemas.auth_service import AccountCreated, AccountUpdated, AccountRoleChanged
from event_schema_registry.schemas.tracker_service import TaskCreated, TaskCompleted, TaskReassigned
import jsonschema
from django.core.management import BaseCommand
import time
from django.conf import settings
import random
from django.db import DatabaseError, transaction
from billing.models import Transaction, BillingCycle
from billing.kafke_producer import dispatch_transaction_created

ACCOUNTS_STREAM = 'accounts_stream'
ACCOUNTS = 'accounts'

TASKS_STREAM = 'tasks_stream'
TASKS = 'tasks'


class Command(BaseCommand):
    help = "Start Reporting Kafka Consumer"

    def handle(self, *args, **kwargs):

        print(settings.KAFKA_BROKER)
        print('steeping 10 sec')
        time.sleep(10)

        consumer = KafkaConsumer(
            bootstrap_servers=[settings.KAFKA_BROKER],
            group_id='billing_service',
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

            # for users username is public_id

            # CUD events
            if event_name == "AccountCreated":
                try:
                    jsonschema.validate(value, AccountCreated.v1)
                    u = User.objects.create(**data)
                    print(u)
                    u.save()
                except Exception as e:
                    print(e)

            elif event_name == "AccountUpdated":
                username = data["username"]
                try:
                    jsonschema.validate(value, AccountUpdated.v1)
                    user = User.objects.get(username=username)
                    user.first_name = data["first_name"]
                    user.last_name = data["last_name"]
                    user.role = data["role"]
                    user.save(update_fields=["role", "first_name", "last_name"])
                    print('AccountUpdated ok')
                except User.DoesNotExist:
                    User.objects.create(**data)
            # Business events
            elif event_name == "AccountRoleChanged":
                try:
                    jsonschema.validate(value, AccountRoleChanged.v1)
                    new_role = data["role"]
                    username = data["username"]
                    user = User.objects.get(username=username)
                    user.role = new_role
                    user.save(update_fields=["role"])
                    print('AccountRoleChanged ok')
                except User.DoesNotExist:
                    User.objects.create(**message.value["data"])



            elif event_name == "TaskCreated" and event_version == 2:
                try:
                    print('TaskCreated v2')
                    jsonschema.validate(value, TaskCreated.v2)

                    # jira_id - validated in schema
                    # additional validation for description
                    if '[' in data['description']:
                        raise Exception('description contains invalid symbol')

                    assignee = User.objects.get(username=data['assignee_username'])

                    fee = random.randint(10, 20),
                    reward = random.randint(20, 40),
                    with transaction.atomic():
                        # создаем задачу с ценами
                        task = Task.objects.create(
                            public_id=data['public_id'],
                            description=data['description'],
                            status=data['status'],
                            assignee=assignee,
                            fee=fee,
                            reward=reward,
                        )
                        print(task)
                        task.save()

                        # тут будет Exception, если он один или их много
                        billing_cycle = BillingCycle.objects.get(active=True)

                        tr = Transaction.objects.create(
                            user = assignee,
                            description = 'Списание денег за ассайн задачи при создании',
                            credit = 0,
                            debit = task.fee,
                            billing_cycle = billing_cycle
                        )

                        # User.update_balance()

                        # TODO dispatch event - Task Assigned (price)

                except Exception as e:
                    # TODO Складываем в DB сломавшееся событие
                    print(e)

            elif event_name == "TaskReassigned":
                print('before try')
                try:
                    jsonschema.validate(value, TaskReassigned.v1)
                    with transaction.atomic():
                        # создаем задачу с ценами
                        task = Task.objects.get(
                            public_id=data['public_id'],
                        )

                        assignee = User.objects.get(username=data['assignee_username'])
                        task.assignee = assignee

                        print(task)
                        task.save()

                        # тут будет Exception, если он один или их много
                        billing_cycle = BillingCycle.objects.get(is_active=True)

                        tr = Transaction.objects.create(
                            user=assignee,
                            description='Списание денег за ассайн задачи при реассайне',
                            credit=0,
                            debit=task.fee,
                            billing_cycle=billing_cycle
                        )
                        print(tr)
                        # User.update_balance()
                        # Todo dispatch event transaction created
                        dispatch_transaction_created(tr)
                except Exception as e:
                    print(e)
            elif event_name == "TaskCompleted":
                try:
                    jsonschema.validate(value, TaskCompleted.v1)

                    with transaction.atomic():
                        task = Task.objects.get(public_id=data['public_id'])

                        # start transaction
                        # draft
                        task.status = Task.Status.complete
                        task.save()
                        reward = task.reward

                        billing_cycle = BillingCycle.objects.get(active=True)

                        tr = Transaction.objects.create(
                            user=task.assignee,
                            description='Начисление денег за ассайн',
                            credit=reward,
                            debit=0,
                            billing_cycle=billing_cycle
                        )
                        print(tr)

                        # User.update_balance()

                        # TODO dispatch event - Task Complete (price)

                except Exception as e:
                    print(e)
                    # store exceptions to special database model
                    # - exception_name
                    # - exception_text
                    # - event_data{}

                    # raise alert / send to sentry
                    # дальше можно разбирать вручную, что не учли

