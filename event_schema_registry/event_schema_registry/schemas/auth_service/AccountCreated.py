v1 = {
    "type": "object",
    "properties": {
        "event_version": { "type": "string" },
        "event_name": { "type": "string" },
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
