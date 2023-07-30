import pymysql

from DB_Access.DB_connection import connection
from controller.CRUD.user_data_base import users_db
from issuies.network import Network


def get_user(user_name):
    return users_db.get(user_name)


async def add_new_data_to_db(query, val):
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
    print("good from the connection to db ")
    return cursor.lastrowid
