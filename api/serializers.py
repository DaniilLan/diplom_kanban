from board.models import Task, TimeLog
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

class TimeLogSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = TimeLog
        fields = ('task',
                  'minutesSpent',
                  'date',
                  'comment',
                  'owner'
                  )

class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'tasks']
