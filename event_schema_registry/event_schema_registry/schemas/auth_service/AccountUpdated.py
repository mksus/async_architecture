v1 = {
    "title": "AccountUpdated",
    "description": "CUD",
    "properties": {
        "event_name": { "type": "string" },
        "event_version": { "enum": [1] },
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
