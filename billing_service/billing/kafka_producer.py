import json

from kafka import KafkaProducer
from event_schema_registry.schemas.billing_service import TransactionCreated, BillingCycleCreated
import jsonschema
from datetime import datetime
from django.conf import settings

producer = KafkaProducer(
    bootstrap_servers=[settings.KAFKA_BROKER],
    value_serializer=lambda m: json.dumps(m).encode('utf-8'), retries=3,
    api_version=(2, 0),
    max_block_ms=2000
)


ACCOUNTS_STREAM = 'accounts_stream'
ACCOUNTS = 'accounts'

TRANSACTIONS = 'transactions'
BILLING_CYCLE = 'billing_cycle'


def dispatch_transaction_created(transaction):
    event = {
            "event_name": "TansactionCreated",
            "event_version": 1,
            "event_time": str(datetime.now()),
            "producer": "billing_service",
            "data": {
                "public_id": str(transaction.public_id),
                "username": transaction.user.username,
                "description": transaction.description,
                "credit": transaction.credit,
                "debit": transaction.debit,
                "billing_cycle_start_date": str(transaction.billing_cycle.start_date), # using like billing cycle public slug
                "type": transaction.type,
            },
        }
    jsonschema.validate(event, TransactionCreated.v1)
    producer.send(TRANSACTIONS, event)


def dispatch_new_billing_cycle(billing_cycle):
    print('billing cycle being dispatched')
    event = {
        "event_name": "BillingCycleCreated",
        "event_version": 1,
        "event_time": str(datetime.now()),
        "producer": "billing_service",
        "data": {
            "start_date": billing_cycle.start_date,
        },
    }

    jsonschema.validate(event, BillingCycleCreated.v1)
    producer.send(BILLING_CYCLE, event)
