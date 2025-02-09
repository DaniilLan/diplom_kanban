from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TaskSerializer, TimeLogSerializer
from board.models import Task, TimeLog
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

class TimeLogList(generics.ListCreateAPIView):
    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return TimeLog.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TimeLogByTask(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, task_uuid):
        timelogs = TimeLog.objects.filter(task=task_uuid, owner=request.user)
        serializer = TimeLogSerializer(timelogs, many=True)
        return Response(serializer.data)

class DetailTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)

    def perform_destroy(self, instance):
        # Сохранение информации об удаляемой задаче
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