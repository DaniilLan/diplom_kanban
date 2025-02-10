# Импортируем необходимые модели
from board.models import Task, TimeLog
from django.contrib.auth.models import User

# Получаем задачу с task_id = 105
task = Task.objects.get(task_id=105)

# Получаем пользователя, который будет владельцем записи в TimeLog
# Например, возьмем первого пользователя в базе данных
owner = User.objects.first()

# Создаем запись в TimeLog
time_log_entry = TimeLog.objects.create(
    task=task,  # Связываем запись с задачей
    owner=owner,  # Указываем владельца записи
    minutesSpent=235,  # Указываем затраченное время в минутах
    comment="Пример 3-го комментария к записи в логе времени"  # Добавляем комментарий
)

# Сохраняем запись в базе данных
time_log_entry.save()

# Выводим информацию о созданной записи
print(f"Создана запись в TimeLog: {time_log_entry}")