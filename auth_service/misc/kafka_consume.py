from kafka import KafkaConsumer
import json


# consumer = KafkaConsumer('accounts_stream',
#                          bootstrap_servers=['localhost:9092'])

#

# for message in consumer:
#     # message value and key are raw bytes -- decode if necessary!
#     # e.g., for unicode: `message.value.decode('utf-8')`
#     print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                           message.offset, message.key,
#                                           message.value))

consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    group_id='async_arc',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    api_version=(2, 0)
)

consumer.subscribe(topics=["accounts", "accounts_stream"])

for message in consumer:
    value = message.value
    event_name = value["event_name"]
    print(value)
    print(event_name)
