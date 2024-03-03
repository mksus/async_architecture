from django.urls import path, include
from .views import create_task


# клиентское приложение
urlpatterns = [
    path("create_task/", create_task, name='create_task'),
]
