v1 = {
    "title": "AccountRoleChanged",
    "description": "BE",
    "type": "object",
    "properties": {
        "event_version": { "type": "string" },
        "event_name": { "type": "string" },
        "event_time": { "type": "string" },
        "producer": { "type": "string" },
        "data": {
            "type": "object",
            "properties": {
                "role": { "type": "string" },
                "username": { "type": "string" },
            }
        },
    }
}
