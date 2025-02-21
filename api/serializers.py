from board.models import Task, TimeLog
from django.contrib.auth.models import User
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('uuid',
                  'task_id',
                  'name',
                  'boardName',
                  'date',
                  'owner',
                  'description',
                  'typeTask',
                  'priorityTask',
                  'timeEstimateMinutes',
                  )


class TimeLogSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = TimeLog
        fields = (
            'uuid',
            'task',
            'minutesSpent',
            'date',
            'comment',
            'owner',
            'owner_username'
        )
        read_only_fields = ('owner', 'date', 'uuid', 'task')  # Добавить task сюда
        extra_kwargs = {
            'minutesSpent': {'required': True},
            'comment': {'required': False}
        }


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'tasks']


