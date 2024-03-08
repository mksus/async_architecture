import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8'), retries=3,
    api_version=(2, 0)
)


ACCOUNTS_STREAM = 'accounts_stream'
ACCOUNTS = 'accounts'


def serialize_account_created(data):
    return {
            "event_name": "AccountCreated",
            "data": {
                "email": data.get("email"),
                "role": data.get("role"),
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "username": data.get("username"),
            },
        }


def serialize_role_changed(data):
    return {
                "event_name": "AccountRoleChanged",
                "data": {
                    "username": data.get("username"),
                    "role": data.get("role"),
                },
            }


def serialize_account_changed(data):
    return {
        "event_name": "AccountChanged",
        "data": {
            "username": data.get("username"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
        },
    }
