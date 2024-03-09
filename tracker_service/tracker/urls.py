from django.urls import path, include
from .views import CreateTaskView, MyTasksView, CompleteTaskView, ReassignTasksView

urlpatterns = [
    path("create/", CreateTaskView.as_view(), name="create_task"),
    path("my_tasks/", MyTasksView.as_view(), name="get_my_tasks"),
    path("reassign/", ReassignTasksView.as_view(), name="reassign_tasks"),
    path("complete/", CompleteTaskView.as_view(), name="complete_task"),
]
