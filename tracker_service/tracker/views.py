from rest_framework import generics, serializers, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tracker.models import Task
from auth_client.models import User
import random


class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.CharField(required=False)

    class Meta:
        model = Task
        fields = ("description", "status", "assignee")


class CreateTaskView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        assignee_queryset = User.objects.exclude(
                role__in=[User.Role.manager.value, User.Role.admin.value]
            )
        if assignee_queryset.exists():
            total_assignees = assignee_queryset.count()
            random_index = random.randint(0, total_assignees - 1)
            assignee = assignee_queryset[random_index]
            serializer.validated_data["assignee"] = assignee
        serializer.validated_data["fee"] = random.randint(10, 20)
        serializer.validated_data["reward"] = random.randint(20, 40)
        serializer.save()


class ReassignTasksView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        opened_tasks = Task.objects.filter(status=Task.Status.open.value)
        for task in opened_tasks:
            assignee_queryset = User.objects.exclude(
                role__in=[User.Role.manager.value, User.Role.admin.value]
            )

            if assignee_queryset.exists():
                total_assignees = assignee_queryset.count()
                random_index = random.randint(0, total_assignees - 1)
                assignee = assignee_queryset[random_index]
                task.assignee = assignee
                task.save()

        serializer = TaskSerializer(opened_tasks, many=True)
        return Response(serializer.data)


class CompleteTaskView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task_id = request.data.get("task_id")
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response("Does not exist", status=404)

        if task.assignee != request.user:
            return Response("Can complete only owned tasks", status=403)

        task.status = Task.Status.complete.value
        task.save(update_fields=["status"])
        return Response(status=200, data="ok")


class MyTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)
