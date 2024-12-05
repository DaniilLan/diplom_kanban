from api.serializers import TaskSerializer

from board.models import Task
from board.models import DeletedTask
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class ListTask(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)

    def perform_destroy(self, instance):
        # Сохранение информации о удаляемой задаче
        DeletedTask.objects.create(
            owner=instance.owner,  # Сохраняем владельца задачи
            task_id=instance.task_id,  # Используем id задачи
            name=instance.name,  # Сохраняем название задачи
            description=instance.description,  # Сохраняем описание задачи
            typeTask=instance.typeTask,  # Сохраняем тип задачи
            priorityTask=instance.priorityTask, # Сохраняем приоритет задачи
        )
        # Удаление оригинальной задачи
        instance.delete()