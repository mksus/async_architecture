v1 = {
    "title": "BalanceChanged",
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
                "username": { "type": "string" },
                "balance": { "type": "integer" },
                "billing_cycle_start_date": { "type": "string" },
            }
        },
    }
}
