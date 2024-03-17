v1 = {
    "title": "TransactionCreated",
    "description": "BE",
    "type": "object",
    "properties": {
        "event_name": {"type": "string"},
        "event_version": {"enum": [1]},
        "event_time": { "type": "string" },
        "producer": { "type": "string" },
        "data": {
            "type": "object",
            "properties": {
                "public_id": { "type": "string" },
                "username": { "type": "string" },
                "description": { "type": "string" },
                "credit": { "type": "integer" },
                "debit": { "type": "integer" },
                "cycle_start_date": { "type": "string" }, # using like billing cycle public slug
                "type": { "type": "string" },
            }
        },
    }
}
