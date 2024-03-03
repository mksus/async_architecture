from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


# todo добавить role, public_id, заполнять их в kafka consumer
