import uuid
from django.db import models
from django.db.models import Max

class BoardNames(models.TextChoices):
    ToDo = 'Сделать'
    ReOpen = 'Переоткрыто'
    InProgress = 'В работе'
    Review = 'На проверке'
    InTest = 'В тестировании'
    Done = 'Выполнено'


class TaskType(models.TextChoices):
    TASK = 'task', 'Задача'
    BUG = 'bug', 'Баг'


class PriorityTask(models.TextChoices):
    HIGH = 'high', 'Высокий'
    MEDIUM = 'medium', 'Средний'
    LOW = 'low', 'Низкий'

class DeletedTask(models.Model):

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='deleted_tasks')
    task_id = models.PositiveIntegerField(unique=True)  # task_id удаленной задачи
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True, verbose_name="Подробное описание")
    delete_date = models.DateTimeField(auto_now_add=True)
    typeTask = models.CharField(max_length=4, choices=TaskType.choices, null=True, blank=True)
    priorityTask = models.CharField(max_length=6, choices=PriorityTask.choices, null=True, blank=True)
    timeEstimateMinutes = models.PositiveIntegerField(null=True, blank=True, verbose_name="Оценка времени (в минутах)")

    class Meta:
        verbose_name = 'Удаленная задача'
        verbose_name_plural = 'Удаленные задачи'

class Group(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='owned_groups', verbose_name="Владелец группы")
    name = models.CharField(max_length=255, verbose_name="Название группы")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'Группа досок'
        verbose_name_plural = 'Группы досок'

    def __str__(self):
        return self.name

class UsersGroup(models.Model):
    uuid = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members', verbose_name="Группа")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='group_memberships', verbose_name="Пользователь")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата присоединения")

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники групп'
        unique_together = ('group', 'user')  # Один пользователь не может быть в группе дважды

    def __str__(self):
        return f"{self.user.username} в {self.group.name}"


class Task(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')
    responsible = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks', verbose_name="Ответственный")
    groups = models.ManyToManyField(Group, related_name='tasks', verbose_name="Группы", blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    task_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=500)
    boardName = models.CharField(max_length=15, choices=BoardNames.choices, default=BoardNames.ToDo)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, verbose_name="Подробное описание")
    typeTask = models.CharField(max_length=4, choices=TaskType.choices, null=True, blank=True)
    priorityTask = models.CharField(max_length=6, choices=PriorityTask.choices, null=True, blank=True)
    timeEstimateMinutes = models.PositiveIntegerField(null=True, blank=True, verbose_name="Оценка времени (в минутах)")


    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def save(self, *args, **kwargs):
        # Генерируем task_id только для новых задач
        if self.task_id is None:
            # Получаем максимальное значение task_id из базы задач и удаленных задач
            max_task_id = Task.objects.aggregate(Max('task_id'))['task_id__max'] or 0
            max_deleted_task_id = DeletedTask.objects.aggregate(Max('task_id'))['task_id__max'] or 0

            # Устанавливаем task_id
            self.task_id = max(max_task_id, max_deleted_task_id) + 1

        super().save(*args, **kwargs)  # Сохраняем объект

    def __str__(self):
        return f"{self.name} (T-{self.task_id})"

class TimeLog(models.Model):
    uuid = models.UUIDField(  # Добавить это поле
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='timelogs')
    minutesSpent = models.PositiveIntegerField(verbose_name="Затраченное время (в минутах)")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата записи")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = 'Лог времени'
        verbose_name_plural = 'Логи времени'

    def __str__(self):
        return f"{self.task.name} - {self.minutesSpent} минут ({self.owner.username})"

