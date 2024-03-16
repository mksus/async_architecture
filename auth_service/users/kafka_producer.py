import json

from kafka import KafkaProducer
from event_schema_registry.schemas.auth_service import AccountCreated, AccountUpdated, AccountRoleChanged
import jsonschema
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8'), retries=3,
    api_version=(2, 0)
)


ACCOUNTS_STREAM = 'accounts_stream'
ACCOUNTS = 'accounts'


def dispatch_account_created(user):
    event = {
            "event_name": "AccountCreated",
            "event_version": 1,
            "event_time": str(datetime.now()),
            "producer": "auth_server",
            "data": {
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
            },
        }
    jsonschema.validate(event, AccountCreated.v1)
    producer.send(ACCOUNTS_STREAM, event)


def dispatch_account_updated(user):
    event = {
        "event_name": "AccountUpdated",
        "event_version": 1,
        "event_time": str(datetime.now()),
        "producer": "auth_server",
        "data": {
            "username": user.username,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    }
    jsonschema.validate(event, AccountUpdated.v1)
    producer.send(ACCOUNTS_STREAM, event)


def dispatch_role_changed(user):
    event = {
        "event_name": "AccountRoleChanged",
        "event_version": 1,
        "event_time": str(datetime.now()),
        "producer": "auth_server",
        "data": {
            "username": user.username,
            "role": user.role,
            },
        }
    jsonschema.validate(event, AccountRoleChanged.v1)
    producer.send(ACCOUNTS, event)


