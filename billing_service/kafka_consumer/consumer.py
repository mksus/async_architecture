def run():
    from kafka import KafkaConsumer
    import json
    from auth_client.models import User
    from billing.models import Task

    import event_schema_registry.schemas.auth_service.AccountCreated as account_created_registry
    from event_schema_registry.schemas.auth_service import AccountCreated, AccountUpdated, AccountRoleChanged
    import jsonschema

    ACCOUNTS_STREAM = 'accounts_stream'
    ACCOUNTS = 'accounts'

    TASKS_STREAM = 'tasks_stream'
    TASKS = 'tasks'


    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        group_id='async_arc',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        api_version=(2, 0)
    )

    consumer.subscribe(topics=[ACCOUNTS, ACCOUNTS_STREAM, TASKS_STREAM, TASKS])

    for message in consumer:
        value = message.value
        event_name = value["event_name"]
        data = value["data"]
        print("Received message: {}".format(value))

        # for users username is public_id

        # CUD events
        if event_name == "AccountCreated":
            try:
                jsonschema.validate(value, AccountCreated.v1)
                u = User.objects.create(**data)
                print(u)
                u.save()
            except Exception as e:
                print(e)

        elif event_name == "AccountUpdated":
            username = data["username"]
            try:
                jsonschema.validate(value, AccountUpdated.v1)
                user = User.objects.get(username=username)
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.role = data["role"]
                user.save(update_fields=["role", "first_name", "last_name"])
                print('AccountUpdated ok')
            except User.DoesNotExist:
                User.objects.create(**data)

        # Business events
        elif event_name == "AccountRoleChanged":
            try:
                jsonschema.validate(value, AccountRoleChanged.v1)
                new_role = data["role"]
                username = data["username"]
                user = User.objects.get(username=username)
                user.role = new_role
                user.save(update_fields=["role"])
                print('AccountRoleChanged ok')
            except User.DoesNotExist:
                User.objects.create(**message.value["data"])

        elif event_name == "TaskCreated":
            try:
                # jsonschema.validate(value, account_created_registry.v1)
                assignee = User.objects.get(username=data['assignee_username'])
                u = Task.objects.create(
                    description=data['descriptions'],
                    status=data['status'],
                    assignee=assignee,
                )
                print(u)
                u.save()
            except Exception as e:
                print(e)

run()
