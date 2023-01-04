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


def check_availability(name: str, shift_id: int, room_id: int):
    with to_connect() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT `accessible` FROM schedules WHERE `name` = %s AND shifts_id = %s AND shifts_rooms_id = %s"
            cursor.execute(sql, (name, shift_id, room_id))
            result = cursor.fetchone()

            return True if result['accessible'] == 0 else False


def make_reservation(name: str, shift_id: int, room_id: int):
    with to_connect() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE schedules SET `accessible` = 1 WHERE `name` = %s AND shifts_id = %s AND shifts_rooms_id = %s"
            cursor.execute(sql, (name, shift_id, room_id))
            connection.commit()


def cancel_reservation(name: str, shift_id: int, room_id: int):
    with to_connect() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE schedules SET `accessible` = 0 WHERE `name` = %s AND shifts_id = %s AND shifts_rooms_id = %s"
            cursor.execute(sql, (name, shift_id, room_id))
            connection.commit()
