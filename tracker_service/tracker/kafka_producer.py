import json

from kafka import KafkaProducer
from event_schema_registry.schemas.tracker_service import TaskCreated, TaskCompleted, TaskReassigned
import jsonschema
from datetime import datetime
from django.conf import settings

producer = KafkaProducer(
    bootstrap_servers=[settings.KAFKA_BROKER],
    value_serializer=lambda m: json.dumps(m).encode('utf-8'), retries=3,
    api_version=(2, 0),
    max_block_ms=2000
)


TASKS_STREAM = 'tasks_stream'
TASKS = 'tasks'


def dispatch_task_created(task):
    event = {
            "event_name": "TaskCreated",
            "event_version": 2,
            "event_time": str(datetime.now()),
            "producer": "auth_server",
            "data": {
                "public_id": str(task.public_id),
                "description": task.description,
                "jira_id": 'stub_jira_id',
                "assignee_username": task.assignee.username,  # user_public_id
                "status": task.status,
            },
        }
    jsonschema.validate(event, TaskCreated.v2)
    producer.send(TASKS_STREAM, event)


def dispatch_task_completed(task):
    event = {
            "event_name": "TaskCompleted",
            "event_version": 1,
            "event_time": str(datetime.now()),
            "producer": "auth_server",
            "data": {
                "public_id": str(task.public_id),
                "description": task.description,
                "assignee_username": task.assignee.username,  # public_id
                "status": task.status,
            },
        }

    try:
        jsonschema.validate(event, TaskCompleted.v1)
        producer.send(TASKS, event)
    except Exception as e:
        # по-хорошему, здесь можно прикрутить outbox_pattern на случай ошибок брокера

        # кртоме того, если мы сломали контракт и валидация отвалилась уже здесь,
        # можно попробовать писать события в отдельню таблицу аналигчсно консьюмеру,
        # чтобы можно было их потом доотправить

        # такой подход может заменить также outbox_pattern на маленьком объеме (наверно, это и есть logtailing)
        print(e)


def dispatch_task_reassigned(task):
    event = {
        "event_name": "TaskReassigned",
        "event_version": 1,
        "event_time": str(datetime.now()),
        "producer": "auth_server",
        "data": {
            "public_id": str(task.public_id),
            "assignee_username": task.assignee.username,  # public_id
        },
    }

    try:
        jsonschema.validate(event, TaskReassigned.v1)
        producer.send(TASKS, event)
    except Exception as e:
        print(e)
