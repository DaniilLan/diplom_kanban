import os
import uuid
from django.utils import timezone

# Важно: сначала установить переменные окружения, потом импортировать Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanban.settings')  # Укажите правильное имя вашего Django-проекта

import django
django.setup()

from django.contrib.auth.models import User
from board.models import (
    BoardNames, TaskType, PriorityTask, Group,
    UsersGroup, Task, TimeLog
)
def create_test_data():
    # Создаем тестового пользователя
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'is_active': True
        }
    )
    if created:
        user.set_password('testpassword123')
        user.save()

    # Создаем группу для дипломного проекта
    group, _ = Group.objects.get_or_create(
        owner=user,
        name='Дипломный проект',
        defaults={'date_created': timezone.now()}
    )

    # Добавляем пользователя в группу
    UsersGroup.objects.get_or_create(
        group=group,
        user=user,
        defaults={'date_joined': timezone.now()}
    )

    # Список задач для каждой колонки
    tasks_data = {
        BoardNames.ToDo: [
            {'name': 'Разработать UX/UI дизайн канбан-доски', 'description': 'Создать макеты интерфейса с учетом принципов UX/UI', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 480},
            {'name': 'Спроектировать архитектуру БД', 'description': 'Разработать ER-диаграмму для сущностей задач, пользователей и групп', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 360},
            {'name': 'Реализовать модель Task', 'description': 'Создать Django-модель для задач с полями: название, описание, статус, тип, приоритет', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 240},
            {'name': 'Настроить аутентификацию', 'description': 'Реализовать регистрацию и авторизацию пользователей', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 180},
            {'name': 'Исправить баг: не сохраняется приоритет', 'description': 'При создании задачи приоритет не сохраняется в БД', 'typeTask': TaskType.BUG, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 120},
            {'name': 'Добавить цветовые маркеры', 'description': 'Реализовать цветовую индикацию для статусов задач', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.LOW, 'timeEstimateMinutes': 90},
            {'name': 'Создать API для задач', 'description': 'Разработать REST API для работы с задачами', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 300},
        ],
        BoardNames.InProgress: [
            {'name': 'Реализовать drag-and-drop', 'description': 'Добавить функционал перемещения задач между колонками', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 240},
            {'name': 'Разработать главную страницу', 'description': 'Создать шаблон главной страницы с канбан-доской', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 180},
            {'name': 'Исправить баг: некорректное отображение даты', 'description': 'Дата создания задачи отображается в неправильном формате', 'typeTask': TaskType.BUG, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 60},
            {'name': 'Реализовать фильтрацию по группам', 'description': 'Добавить возможность фильтрации задач по группам пользователя', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 120},
            {'name': 'Создать модальное окно для задач', 'description': 'Разработать UI для создания/редактирования задач', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 150},
            {'name': 'Настроить цветовые темы', 'description': 'Реализовать переключение цветовых тем интерфейса', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.LOW, 'timeEstimateMinutes': 90},
            {'name': 'Добавить лог времени', 'description': 'Создать функционал учета затраченного времени', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 180},
        ],
        BoardNames.Review: [
            {'name': 'Проверить работу API', 'description': 'Протестировать все endpoints API для задач', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 120},
            {'name': 'Ревью кода авторизации', 'description': 'Провести код-ревью модуля аутентификации', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 90},
            {'name': 'Тестирование drag-and-drop', 'description': 'Проверить корректность работы перемещения задач', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 60},
            {'name': 'Проверить валидацию форм', 'description': 'Убедиться в корректности валидации данных в формах', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 45},
            {'name': 'Исправить баг: утечка памяти', 'description': 'Обнаружена утечка памяти при частом обновлении доски', 'typeTask': TaskType.BUG, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 180},
            {'name': 'Документирование кода', 'description': 'Проверить полноту и корректность документации', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.LOW, 'timeEstimateMinutes': 120},
            {'name': 'Оптимизация запросов', 'description': 'Проверить оптимизацию SQL-запросов к БД', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 90},
        ],
        BoardNames.InTest: [
            {'name': 'Тестирование на разных устройствах', 'description': 'Проверить отзывчивость интерфейса', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 240},
            {'name': 'Нагрузочное тестирование', 'description': 'Провести тестирование под нагрузкой', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 180},
            {'name': 'Тестирование безопасности', 'description': 'Проверить уязвимости системы', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 150},
            {'name': 'Исправить баг: кэширование', 'description': 'Проблемы с кэшированием данных задач', 'typeTask': TaskType.BUG, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 90},
            {'name': 'Тестирование API', 'description': 'Полное тестирование REST API', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 120},
            {'name': 'Проверка валидации данных', 'description': 'Тестирование обработки неверных данных', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 60},
            {'name': 'Тестирование тем оформления', 'description': 'Проверить работу всех цветовых тем', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.LOW, 'timeEstimateMinutes': 45},
        ],
        BoardNames.Done: [
            {'name': 'Настройка Django проекта', 'description': 'Базовая настройка Django-проекта', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 120},
            {'name': 'Создание ER-диаграммы', 'description': 'Разработка диаграммы сущностей БД', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 180},
            {'name': 'Проектирование архитектуры', 'description': 'Разработка архитектуры веб-приложения', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 240},
            {'name': 'Исправить баг: регистрация', 'description': 'Исправлена ошибка при регистрации новых пользователей', 'typeTask': TaskType.BUG, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 90},
            {'name': 'Диаграмма Use Case', 'description': 'Создана диаграмма вариантов использования', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 150},
            {'name': 'Настройка CI/CD', 'description': 'Настройка процесса непрерывной интеграции', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.HIGH, 'timeEstimateMinutes': 120},
            {'name': 'Документация API', 'description': 'Создана документация для REST API', 'typeTask': TaskType.TASK, 'priorityTask': PriorityTask.MEDIUM, 'timeEstimateMinutes': 90},
        ]
    }

    # Создаем задачи для каждой колонки
    for board_name, tasks in tasks_data.items():
        for task_data in tasks:
            task = Task.objects.create(
                owner=user,
                responsible=user,
                name=task_data['name'],
                boardName=board_name,
                description=task_data['description'],
                typeTask=task_data['typeTask'],
                priorityTask=task_data['priorityTask'],
                timeEstimateMinutes=task_data['timeEstimateMinutes'],
                date=timezone.now()
            )
            task.groups.add(group)
            task.save()

    # Добавляем лог времени для некоторых задач
    time_logs = [
        {'task_name': 'Настройка Django проекта', 'minutes': 120, 'comment': 'Базовая настройка проекта'},
        {'task_name': 'Создание ER-диаграммы', 'minutes': 180, 'comment': 'Разработка диаграммы сущностей'},
        {'task_name': 'Проектирование архитектуры', 'minutes': 240, 'comment': 'Архитектурное проектирование'},
        {'task_name': 'Реализовать drag-and-drop', 'minutes': 60, 'comment': 'Начальная реализация'},
    ]

    for log in time_logs:
        task = Task.objects.filter(name=log['task_name']).first()
        if task:
            TimeLog.objects.create(
                task=task,
                owner=user,
                minutesSpent=log['minutes'],
                comment=log['comment'],
                date=timezone.now()
            )

    print("Тестовые данные успешно созданы!")

if __name__ == '__main__':
    create_test_data()