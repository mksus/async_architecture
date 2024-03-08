from django.urls import path, include
from .views import create_task, reassign_tasks, complete_task


# клиентское приложение
urlpatterns = [
    path("create_task/", create_task, name='create_task'),
    path("reassign_tasks/", reassign_tasks, name='reassign_tasks'),
    path("complete_task/", complete_task, name='complete_task'),
]
