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
        fields = ("public_id", "description", "status", "assignee")
        read_only_fields = ('public_id',)


class CreateTaskView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        assignee_queryset = User.objects.exclude(
                role__in=[User.Role.manager, User.Role.admin]
            )
        if assignee_queryset.exists():
            total_assignees = assignee_queryset.count()
            random_index = random.randint(0, total_assignees - 1)
            assignee = assignee_queryset[random_index]
            serializer.validated_data["assignee"] = assignee
        print("creating task")
        print(serializer.validated_data)
        serializer.save()


class ReassignTasksView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        opened_tasks = Task.objects.filter(status=Task.Status.open)
        for task in opened_tasks:
            assignee_queryset = User.objects.exclude(
                role__in=[User.Role.manager, User.Role.admin]
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
        public_id = request.data.get("public_id")
        try:
            task = Task.objects.get(public_id=public_id)
        except Task.DoesNotExist:
            return Response("Does not exist", status=404)

        if task.assignee != request.user:
            return Response("Can complete only owned tasks", status=403)

        task.status = Task.Status.complete
        task.save(update_fields=["status"])

        serializer = TaskSerializer(task)
        return Response(serializer.data)


class MyTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)
