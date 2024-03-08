from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('my-topic',
                         bootstrap_servers=['localhost:9092'])

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

    json_str = message.value.decode('utf-8')
    print(json.loads(json_str).get('key2'))

    # todo здесь нужно обрабатывать данные про пользователей, создавать их

