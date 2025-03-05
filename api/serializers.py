from board.models import Task, TimeLog, Group
from django.contrib.auth.models import User
from rest_framework import serializers



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
        read_only_fields = ('owner', 'date', 'uuid', 'task')


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'tasks', 'groups']

    def get_groups(self, obj):
        return [group.name for group in obj.group_memberships.all()]


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('uuid', 'name', 'owner', 'date_created', 'members')

    def get_members(self, obj):
        return [user.user.username for user in obj.members.all()]

    def validate(self, data):
        """
        Проверяем, что пользователь имеет доступ к группе.
        """
        user = self.context['request'].user
        if 'members' in data:
            for member in data['members']:
                if member.user != user and not user.is_superuser:
                    raise serializers.ValidationError(
                        "Вы не можете добавлять других пользователей в группу."
                    )
        return data


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        pk_field=serializers.UUIDField()
    )
    responsible = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = (
            'uuid', 'task_id', 'name', 'boardName', 'date', 'owner',
            'description', 'typeTask', 'priorityTask',
            'timeEstimateMinutes', 'groups', 'responsible'
        )

    def validate_groups(self, value):
        """
        Проверяем, что пользователь имеет доступ к указанным группам.
        """
        user = self.context['request'].user
        user_groups = user.group_memberships.values_list('group', flat=True)

        for group in value:
            if group.uuid not in user_groups:
                raise serializers.ValidationError(
                    f"У вас нет доступа к группе {group.name}"
                )
        return value