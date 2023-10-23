import sqlite3


def create_database():
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей (id, имя, номер и количество поинтов)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, user_name TEXT, vpn_number INT, points INT)''')
    conn.commit()

    # Закрыть соединение
    conn.close()


def check_existing_user(user_id):
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверка наличия пользователя в базе данных
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    # Закрыть соединение
    conn.close()

    return existing_user


def write_user_to_db(user_id, user_name, vpn_number, points):
    # Используем менеджер контекста для открытия соединения с базой данных
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        # Вставляем данные пользователя в таблицу users
        cursor.execute("INSERT INTO users (user_id, user_name, vpn_number, points) VALUES (?, ?, ?, ?)",
                       (user_id, user_name, vpn_number, points))

