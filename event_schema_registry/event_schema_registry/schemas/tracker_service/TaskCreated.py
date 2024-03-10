v1 = {
    "title": "TaskCreated",
    "description": "CUD",
    "type": "object",
    "properties": {
        "event_version": { "type": "string" },
        "event_name": { "enum": [1] },
        "event_time": { "type": "string" },
        "producer": { "type": "string" },
        "data": {
            "type": "object",
            "properties": {
                "public_id": { "type": "string" },
                "description": { "type": "string" },
                "assignee_username": { "type": "string" },
                "status": { "type": "string" },
            }
        }
    }
}
