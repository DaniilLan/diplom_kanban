from board.models import Task
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'tasks']
