from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import TaskSerializer, TimeLogSerializer, GroupSerializer
from board.models import Task, TimeLog, Group
from board.models import DeletedTask
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class ListTask(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(owner=user) |
            Q(group__members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        # Получаем первую группу, где пользователь является участником или владельцем
        user_group = Group.objects.filter(
            Q(members__user=self.request.user) |
            Q(owner=self.request.user)
        ).first()

        serializer.save(
            owner=self.request.user,
            group=user_group  # Автоматически устанавливаем группу
        )

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

class TimeLogCreate(generics.CreateAPIView):
    serializer_class = TimeLogSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task = get_object_or_404(
            Task,
            uuid=self.kwargs['task_uuid'],
            owner=self.request.user
        )
        serializer.save(owner=self.request.user, task=task)

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

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(owner=user) |
            Q(group__members__user=user)
        ).distinct()

class GroupList(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(
            Q(owner=self.request.user) |
            Q(members__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(
            Q(owner=self.request.user) |
            Q(members__user=self.request.user)
        ).distinct()
