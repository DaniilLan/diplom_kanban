from board.models import Task
from django.contrib.auth.models import User
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('uuid', 'task_id', 'name', 'boardName', 'date', 'owner', 'description', 'typeTask', 'priorityTask')


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'tasks']
