import sqlite3


def create_database():
    # Подключение к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей (id, имя, номер, количество поинтов и статус valid)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (user_id INTEGER PRIMARY KEY, user_name TEXT, vpn_number INT, 
                          points INT, valid BOOLEAN, on_validation INT)''')

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


def write_user_to_db(user_id, user_name, vpn_number, points, valid=False, on_validation=0):
    # Используем менеджер контекста для открытия соединения с базой данных
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        # Вставляем данные пользователя в таблицу users
        cursor.execute("INSERT INTO users (user_id, user_name, vpn_number, points, valid, on_validation) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, user_name, vpn_number, points, valid, on_validation))


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
        on_validation = int(duration)

        # Обновление полей points и valid в базе данных
        cursor.execute("UPDATE users SET points=?, on_validation=?, valid=0 WHERE user_id=?",
                       (new_points, on_validation, user_id))
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
        # Обновляем поля valid и on_validation в базе данных для данного пользователя
        user_id = user[0]
        cursor.execute("UPDATE users SET valid=?, on_validation=? WHERE user_id=?", (True, 0, user_id))
        conn.commit()
        conn.close()
        return True  # Успешно установлено значение valid=True и on_validation=0
    else:
        conn.close()
        return False  # Пользователь с указанным VPN-номером и validate=False не найден


def set_user_invalid(vpn_num_rejected):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получаем пользователя с указанным VPN-номером
    cursor.execute("SELECT * FROM users WHERE vpn_number=? AND valid=?",(vpn_num_rejected, False))
    user = cursor.fetchone()

    if user:
        user_id, _, _, points, _, on_validation = user
        new_points = points - on_validation  # вычитаем on_validation из points

        # Обновляем поля points и on_validation в базе данных
        cursor.execute("UPDATE users SET points=?, on_validation=0, valid=1 WHERE user_id=?", (new_points, user_id))
        conn.commit()
        conn.close()
        return True  # Успешно установлено значение valid=False и on_validation=0
    else:
        conn.close()
        return False  # Пользователь с указанным VPN-номером и validate=True не найден


def decrease_points():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        with conn:
            cursor.execute("UPDATE users SET points = points - 1 WHERE points > 0")  # Избегаем отрицательных значений
    except Exception as e:
        print(f"Ошибка при выполнении транзакции: {e}")
    finally:
        conn.close()
