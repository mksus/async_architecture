import json

from kafka import KafkaProducer
from event_schema_registry.schemas.tracker_service import TaskCreated, TaskCompleted
import jsonschema
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8'), retries=3,
    api_version=(2, 0)
)


TASKS_STREAM = 'tasks_stream'
TASKS = 'tasks'


def dispatch_task_created(task):
    event = {
            "event_name": "TaskCreated",
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
    jsonschema.validate(event, TaskCreated.v1)
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
        producer.send(TASKS_STREAM, event)
    except Exception as e:
        # по-хорошему, здесь можно прикрутить outbox_pattern на случай ошибок брокера

        # кртоме того, если мы сломали контракт и валидация отвалилась уже здесь,
        # можно попробовать писать события в отдельню таблицу аналигчсно консьюмеру,
        # чтобы можно было их потом доотправить

        # такой подход может заменить также outbox_pattern на маленьком объеме (наверно, это и есть logtailing)
        print(e)
