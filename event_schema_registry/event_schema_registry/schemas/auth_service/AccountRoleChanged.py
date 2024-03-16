v1 = {
    "title": "AccountRoleChanged",
    "description": "BE",
    "type": "object",
    "properties": {
        "event_name": { "type": "string" },
        "event_version": { "enum": [1] },
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
