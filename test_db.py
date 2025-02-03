import sqlite3
from datetime import datetime

def create_timelog_entry(db_path, task_id, owner_id, minutes_spent, date, comment):
    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Преобразуем объект datetime в строку в формате, понятном SQLite
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')

    # SQL-запрос для вставки данных в таблицу board_timelog
    query = """
    INSERT INTO board_timelog (task_id, owner_id, minutesSpent, date, comment)
    VALUES (?, ?, ?, ?, ?)
    """

    # Выполнение запроса с передачей параметров
    cursor.execute(query, (task_id, owner_id, minutes_spent, date_str, comment))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Пример использования метода
db_path = 'db.sqlite3.db'
task_id = 55
owner_id = 1
minutes_spent = 120
date = datetime.now()  # Текущая дата и время
comment = "Worked on the project"

create_timelog_entry(db_path, task_id, owner_id, minutes_spent, date, comment)