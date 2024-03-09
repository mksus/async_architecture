def run():
    from kafka import KafkaConsumer
    import json
    from auth_client.models import User

    ACCOUNTS_STREAM = 'accounts_stream'
    ACCOUNTS = 'accounts'

    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        group_id='async_arc',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        api_version=(2, 0)
    )

    consumer.subscribe(topics=[ACCOUNTS, ACCOUNTS_STREAM])

    for message in consumer:
        value = message.value
        event_name = value["event_name"]
        data = value["data"]
        print("Received message: {}".format(value))

        # for users username is public_id

        # CUD events
        if event_name == "AccountCreated":
            try:
                u = User.objects.create(**message.value["data"])
                print(u)
                u.save()
            except Exception as e:
                print(e)

        elif event_name == "AccountChanged":
            username = data["username"]
            try:
                user = User.objects.get(username=username)
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.role = data["role"]
                user.save(update_fields=["role", "first_name", "last_name"])
            except User.DoesNotExist:
                User.objects.create(**data)

        # Business events
        elif event_name == "AccountRoleChanged":
            new_role = data["role"]
            username = data["username"]
            try:
                user = User.objects.get(username=username)
                user.role = new_role
                user.save(update_fields=["role"])
            except User.DoesNotExist:
                User.objects.create(**message.value["data"])

run()
