import sqlite3


def create_database():
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (user_id INTEGER PRIMARY KEY,
                           user_name TEXT,
                           vpn_number INT, 
                           points INT,
                           need_validation BOOLEAN,
                           on_validation INT,
                           subscription_notification_enabled BOOLEAN)''')

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


def check_need_validation(user_id):
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение значения поля need_validation
    cursor.execute("SELECT need_validation FROM users WHERE user_id=?", (user_id,))
    valid_status = cursor.fetchone()[0]

    return valid_status


def write_user_to_db(user_id, user_name, vpn_number, points, need_validation=False, on_validation=0,
                     subscription_notification_enabled=1):
    # Используем менеджер контекста для открытия соединения с базой данных
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        # Вставляем данные пользователя в таблицу users
        cursor.execute(
            "INSERT INTO users (user_id, user_name, vpn_number, points, need_validation, on_validation,subscription_notification_enabled) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, user_name, vpn_number, points, need_validation, on_validation, subscription_notification_enabled))


def update_user_points(user_id, duration):
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение значения поля need_validation
    cursor.execute("SELECT need_validation FROM users WHERE user_id=?", (user_id,))
    valid_status = cursor.fetchone()[0]

    if valid_status:
        # Закрыть соединение
        conn.close()

        # Возвращаем сигнал об ошибке, если поле valid равно False
        return False

    else:
        # Получение текущего значения points пользователя
        cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
        current_points = cursor.fetchone()[0]

        # Вычисление нового значения points (прибавляем duration)
        new_points = current_points + int(duration)
        on_validation = int(duration)

        # Обновление полей points и valid в базе данных
        cursor.execute("UPDATE users SET points=?, on_validation=?, need_validation=1 WHERE user_id=?",
                       (new_points, on_validation, user_id))
        conn.commit()

        # Закрыть соединение
        conn.close()

        # Возвращаем успешный сигнал
        return True


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
    cursor.execute("SELECT * FROM users WHERE need_validation=?", (True,))
    validate_users = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    return validate_users


def set_user_valid(vpn_number):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверяем наличие пользователя с указанным VPN-номером и need_validation=True
    cursor.execute("SELECT * FROM users WHERE vpn_number=? AND need_validation=?", (vpn_number, True))
    user = cursor.fetchone()
    if user is None:
        return False, None

    user_id = user[0]

    if user:
        # Обновляем поля need_validation и on_validation в базе данных для данного пользователя
        cursor.execute("UPDATE users SET need_validation=?, on_validation=? WHERE user_id=?", (False, 0, user_id))
        conn.commit()
        conn.close()
        return True, user_id  # Успешно установлено значение need_validation=False и on_validation=0
    else:
        conn.close()
        return False, user_id  # Пользователь с указанным VPN-номером и need_validation=True не найден


def set_user_invalid(vpn_num_rejected):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получаем пользователя с указанным VPN-номером
    cursor.execute("SELECT * FROM users WHERE vpn_number=? AND need_validation=?", (vpn_num_rejected, True))
    user = cursor.fetchone()

    if user:
        user_id, _, _, points, _, on_validation, _ = user
        new_points = points - on_validation  # вычитаем on_validation из points

        # Обновляем поля points и on_validation в базе данных
        cursor.execute("UPDATE users SET points=?, on_validation=0, need_validation=0 WHERE user_id=?",
                       (new_points, user_id))
        conn.commit()
        conn.close()
        return True  # Успешно установлено значение need_validation=False и on_validation=0
    else:
        conn.close()
        return False  # Пользователь с указанным VPN-номером и need_validation=True не найден


def get_user_info(user_id):
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение информации о пользователе по его user_id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_info = cursor.fetchone()

    # Закрыть соединение
    conn.close()

    # Если пользователь найден, возвращаем информацию о нем
    if user_info:
        return user_info
    else:
        return None  # Возвращаем None, если пользователь не найден


def decrease_points():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        with conn:
            cursor.execute("UPDATE users SET points = points - 1 WHERE points > 0")  # Избегаем отрицательных значений
    except Exception as e:
        print(f"Ошибка при выполнении транзакции (decrease_points): {e}")
    finally:
        conn.close()


def check_subscription_expiry():
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение пользователей с points <= 3
    cursor.execute(
        "SELECT user_id, points FROM users WHERE points > 0 AND points < 4 AND subscription_notification_enabled = 1")
    users_to_notify = cursor.fetchall()

    # Закрыть соединение
    conn.close()

    return users_to_notify


def toggle_subscription_notification(user_id):
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверка наличия пользователя в базе данных
    cursor.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
    user_exists = cursor.fetchone()

    if user_exists:
        # Получение текущего значения поля subscription_notification_enabled
        cursor.execute("SELECT subscription_notification_enabled FROM users WHERE user_id=?", (user_id,))
        current_value = cursor.fetchone()[0]

        # Инвертирование значения (True становится False, False становится True)
        new_value = not current_value

        # Обновление поля subscription_notification_enabled в базе данных
        cursor.execute("UPDATE users SET subscription_notification_enabled=? WHERE user_id=?", (new_value, user_id))
        # Применение изменений
        conn.commit()

        # Закрыть соединение
        conn.close()

        return new_value
    else:
        # Если пользователя нет в базе данных, возвращаем False или None, чтобы указать об этом
        conn.close()
        return False
