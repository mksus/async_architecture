v1 = {
    "title": "AccountCreated",
    "description": "CUD",
    "type": "object",
    "properties": {
        "event_name": {"type": "string"},
        "event_version": {"enum": [1]},
        "event_time": { "type": "string" },
        "producer": { "type": "string" },
        "data": {
            "type": "object",
            "properties": {
                "email": { "type": "string" },
                "role": { "type": "string" },
                "first_name": { "type": "string" },
                "last_name": { "type": "string" },
                "username": { "type": "string" },
            }
        },
    }
}
