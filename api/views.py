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
            Q(groups__members__user=user)  # Используем groups вместо group
        ).distinct()

    def perform_create(self, serializer):
        # Получаем список UUID групп из запроса
        groups_uuids = self.request.data.get('groups', [])
        groups = Group.objects.filter(uuid__in=groups_uuids)

        serializer.save(
            owner=self.request.user,
            groups=groups.all()  # Сохраняем все выбранные группы
        )


class TimeLogList(generics.ListCreateAPIView):
    serializer_class = TimeLogSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_tasks = Task.objects.filter(
            Q(owner=user) |
            Q(groups__members__user=user)
        ).distinct()

        return TimeLog.objects.filter(task__in=accessible_tasks)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TimeLogsByTask(generics.ListAPIView):
    serializer_class = TimeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_uuid = self.kwargs['task_uuid']
        task = get_object_or_404(Task, uuid=task_uuid)
        user = self.request.user

        if (
                task.owner != user
                and not task.groups.filter(members__user=user).exists()
        ):
            raise PermissionDenied("У вас нет доступа к этой задаче.")

        return TimeLog.objects.filter(task=task)


class TimeLogCreate(generics.CreateAPIView):
    serializer_class = TimeLogSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task = get_object_or_404(Task, uuid=self.kwargs['task_uuid'])
        if (
                task.owner != self.request.user
                and not task.groups.filter(members__user=self.request.user).exists()
        ):
            raise PermissionDenied("У вас нет доступа к этой задаче.")

        serializer.save(owner=self.request.user, task=task)

class DetailTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(owner=user) |
            Q(groups__members__user=user)  # Используем groups вместо group
        ).distinct()

    def perform_destroy(self, instance):
        # Проверяем существование записи перед созданием
        if not DeletedTask.objects.filter(task_id=instance.task_id).exists():
            DeletedTask.objects.create(
                owner=instance.owner,
                task_id=instance.task_id,
                name=instance.name,
                description=instance.description,
                typeTask=instance.typeTask,
                priorityTask=instance.priorityTask,
                timeEstimateMinutes=instance.timeEstimateMinutes
            )
        instance.delete()

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
