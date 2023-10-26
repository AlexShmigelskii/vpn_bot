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


def check_valid(user_id):
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение значения поля valid
    cursor.execute("SELECT valid FROM users WHERE user_id=?", (user_id,))
    valid_status = cursor.fetchone()[0]

    return valid_status


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

    # Получение значения поля valid
    cursor.execute("SELECT valid FROM users WHERE user_id=?", (user_id,))
    valid_status = cursor.fetchone()[0]

    if valid_status:
        # Получение текущего значения points пользователя
        cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
        current_points = cursor.fetchone()[0]

        # Вычисление нового значения points (прибавляем duration)
        new_points = current_points + int(duration)

        # Обновление полей points и valid в базе данных
        cursor.execute("UPDATE users SET points=?, valid=0 WHERE user_id=?", (new_points, user_id))
        conn.commit()

        # Закрыть соединение
        conn.close()

        # Возвращаем успешный сигнал
        return True
    else:
        # Закрыть соединение
        conn.close()

        # Возвращаем сигнал об ошибке, если поле valid равно False
        return False


def update_user_vpn_num(user_id, vpn_number):
    vpn_number = int(vpn_number)
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверка наличия номера vpn в базе данных
    cursor.execute("SELECT * FROM users WHERE vpn_number=?", (vpn_number,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Номер vpn уже существует в базе данных, возвращаем ошибку
        conn.close()
        return "ERROR: Номер vpn уже занят. Пожалуйста, введите свой номер."

    # Обновление поля vpn_number в базе данных
    cursor.execute("UPDATE users SET vpn_number=? WHERE user_id=?", (vpn_number, user_id))
    conn.commit()

    # Закрыть соединение
    conn.close()

    # Возвращаем успешный сигнал
    return "Номер vpn успешно обновлен."


def get_all_users():
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение всех пользователей из базы данных
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Закрыть соединение
    conn.close()

    return users


def get_validate_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Выбираем пользователей с validate=False
    cursor.execute("SELECT * FROM users WHERE valid=?", (False,))
    validate_users = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    return validate_users


def set_user_valid(vpn_number):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверяем наличие пользователя с указанным VPN-номером и validate=False
    cursor.execute("SELECT * FROM users WHERE vpn_number=? AND valid=?", (vpn_number, False))
    user = cursor.fetchone()

    if user:
        # Обновляем поле valid в базе данных для данного пользователя
        user_id = user[0]
        cursor.execute("UPDATE users SET valid=? WHERE user_id=?", (True, user_id))
        conn.commit()
        conn.close()
        return True  # Успешно установлено значение valid=True
    else:
        conn.close()
        return False  # Пользователь с указанным VPN-номером и validate=False не найден
