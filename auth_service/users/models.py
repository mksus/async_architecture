from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


# todo добавить role и public_id
# todo сделать post_save signal на отправку CUD данных по юзеру