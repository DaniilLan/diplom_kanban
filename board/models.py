import uuid
from django.db import models
from django.db.models import Max


class BoardNames(models.TextChoices):
    ToDo = 'Сделать'
    InProgress = 'В процессе'
    Review = 'На проверке'
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

    class Meta:
        verbose_name = 'Удаленная задача'
        verbose_name_plural = 'Удаленные задачи'


class Task(models.Model):

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    task_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=500)
    boardName = models.CharField(max_length=12, choices=BoardNames.choices, default=BoardNames.ToDo)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, verbose_name="Подробное описание")
    typeTask = models.CharField(max_length=4, choices=TaskType.choices, null=True, blank=True)
    priorityTask = models.CharField(max_length=6, choices=PriorityTask.choices, null=True, blank=True)

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

