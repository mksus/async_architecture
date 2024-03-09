from jsonschema import validate

schema = {
  "title": "User.Created.v1",
  "description": "json schema for billing refund event (version 1)",

  "type": "object",

  "properties": {
    "user_id":      { "type": "string" },
    "event_version": { "enum": [1] },
    "event_name":    { "type": "string" },
    "event_time":    { "type": "string" },
    "producer":      { "type": "string" },
  },

  "required": [
    "user_id"
  ]
}


result = validate(
  {"user_id": "some"},
  schema
)

print(result)
