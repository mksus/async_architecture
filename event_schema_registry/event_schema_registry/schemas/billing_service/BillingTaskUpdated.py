v1 = {
    "title": "BillingTaskUpdated",
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
                "fee": { "type": "integer" },
                "reward": { "type": "integer" },
            }
        },
    }
}
