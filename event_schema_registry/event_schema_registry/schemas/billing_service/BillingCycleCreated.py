v1 = {
    "title": "BillingCycleCreated",
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
                "start_dtae": { "type": "string" },
            }
        },
    }
}
