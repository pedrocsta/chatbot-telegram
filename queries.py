from contextlib import contextmanager

import pymysql.cursors


@contextmanager
def to_connect() -> None:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        db='chatbot_telegram',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        yield connection
    finally:
        connection.close()


def check_user(username: str):
    with to_connect() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT username FROM users WHERE `username` = %s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()

            return False if result == None else True


def check_availability(name: str, shift_id: int, room_id: int) -> bool:
    with to_connect() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT `accessible`, booked_by FROM schedules WHERE `name` = %s AND shifts_id = %s AND shifts_rooms_id = %s"
            cursor.execute(sql, (name, shift_id, room_id))
            result = cursor.fetchone()

            return True if result['accessible'] == 0 else False, result['booked_by']


def make_reservation(name: str, shift_id: int, room_id: int, associate: str) -> None:
    with to_connect() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE schedules SET `accessible` = 1, booked_by = %s WHERE `name` = %s AND shifts_id = %s AND shifts_rooms_id = %s"
            cursor.execute(sql, (associate, name, shift_id, room_id))
            connection.commit()


def cancel_reserve(name: str, shift_id: int, room_id: int) -> None:
    with to_connect() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE schedules SET `accessible` = 0, booked_by = '' WHERE `name` = %s AND shifts_id = %s AND shifts_rooms_id = %s"
            cursor.execute(sql, (name, shift_id, room_id))
            connection.commit()


if __name__ == '__main__':
    result = check_availability('primeiro', 1, 1)
    print(result[0], result[1])
