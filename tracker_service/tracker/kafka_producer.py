import json

from kafka import KafkaProducer
import event_schema_registry.schemas.auth_service.AccountCreated as reg
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
            "event_version": "1",
            "event_time": str(datetime.now()),
            "producer": "auth_server",
            "data": {
                "description": task.description,
                "assignee_username": task.assignee.username,  # public_id
                "status": task.status,
            },
        }
    # jsonschema.validate(event, reg.v1)
    producer.send(TASKS_STREAM, event)


# def dispatch_role_changed(user):
#     event = {
#                 "event_name": "AccountRoleChanged",
#                 "data": {
#                     "username": user.username,
#                     "role": user.role,
#                 },
#             }
#     producer.send(ACCOUNTS, event)
#
#
# def dispatch_account_changed(user):
#     event = {
#         "event_name": "AccountChanged",
#         "data": {
#             "username": user.username,
#             "role": user.role,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#         },
#     }
#     producer.send(ACCOUNTS_STREAM, event)
