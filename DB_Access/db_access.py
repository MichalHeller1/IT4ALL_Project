import pymysql

from DB_Access.DB_connection import connection


async def add_new_data_to_db(query, val):
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
    return cursor.lastrowid


async def get_data_from_db(query, val):
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        data = cursor.fetchone()
    return data


async def get_network_connections_from_db(query, val):
    print("i am in the get_network_connections_from_db func")
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
        connections_in_network = cursor.fetchall()
    print("got all connections")
    return connections_in_network


async def get_client_devices_from_db(query, val):
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
        devices = cursor.fetchall()
        return devices


async def invoke_query(query, val):
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
        result_from_db = cursor.fetchall()
        return result_from_db
