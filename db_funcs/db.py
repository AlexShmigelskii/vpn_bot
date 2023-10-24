import sqlite3


def create_database():
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей (id, имя, номер, количество поинтов и статус valid)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, user_name TEXT, vpn_number INT, points INT, valid BOOLEAN)''')
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


def write_user_to_db(user_id, user_name, vpn_number, points, valid=False):
    # Используем менеджер контекста для открытия соединения с базой данных
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        # Вставляем данные пользователя в таблицу users
        cursor.execute("INSERT INTO users (user_id, user_name, vpn_number, points, valid) VALUES (?, ?, ?, ?, ?)",
                       (user_id, user_name, vpn_number, points, valid))


def update_user_points(user_id, duration):
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение текущего значения points пользователя
    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    current_points = cursor.fetchone()[0]

    # Вычисление нового значения points (прибавляем duration)
    new_points = current_points + int(duration)

    # Обновление поля points в базе данных
    cursor.execute("UPDATE users SET points=? WHERE user_id=?", (new_points, user_id))
    conn.commit()

    # Закрыть соединение
    conn.close()


def update_user_vpn_num(user_id, vpn_number):
    vpn_number = int(vpn_number)
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Обновление поля vpn_number в базе данных
    cursor.execute("UPDATE users SET vpn_number=? WHERE user_id=?", (vpn_number, user_id))
    conn.commit()

    # Закрыть соединение
    conn.close()
