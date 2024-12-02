import uuid
from django.db import models

class Task(models.Model):
    class boardNames(models.TextChoices):
        ToDo = 'Сделать'
        InProgress = 'В процессе'
        Review = 'На проверке'
        Done = 'Выполнено'

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    task_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=500)
    boardName = models.CharField(max_length=12, choices=boardNames.choices, default=boardNames.ToDo)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, verbose_name="Подробное описание")

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def save(self, *args, **kwargs):
        # Генерируем task_id только для новых задач
        if self.task_id is None:
            # Получаем максимальное значение task_id из базы
            max_task_id = Task.objects.aggregate(models.Max('task_id'))['task_id__max'] or 0
            self.task_id = max_task_id + 1
        super().save(*args, **kwargs)  # Сохраняем объект

    def __str__(self):
        return f"{self.name} (T-{self.task_id})"
