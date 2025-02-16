# Импортируем необходимые модели
from board.models import Task, TimeLog
from django.contrib.auth.models import User

# Получаем задачу с task_id = 105
task = Task.objects.get(task_id=124)

# Получаем пользователя, который будет владельцем записи в TimeLog
# Например, возьмем первого пользователя в базе данных
owner = User.objects.first()

# Создаем запись в TimeLog
time_log_entry = TimeLog.objects.create(
    task=task,  # Связываем запись с задачей
    owner=owner,  # Указываем владельца записи
    minutesSpent=684,  # Указываем затраченное время в минутах
    comment="Пример 5-го комментария к записи в логе времени"
            "444 444444 4444 444444 444 444444444 4444 44444444444"  # Добавляем комментарий
)

# Сохраняем запись в базе данных
time_log_entry.save()

# Выводим информацию о созданной записи
print(f"Создана запись в TimeLog: {time_log_entry}")