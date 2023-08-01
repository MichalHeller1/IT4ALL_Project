from DB_Access.DB_connection import connection
import codecs


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
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
        connections_in_network = cursor.fetchall()

    decoded_connections = []
    for con in connections_in_network:
        decoded_connection = []
        for item in con:
            if isinstance(item, bytes):
                decoded_connection.append(codecs.decode(item, 'latin-1'))
            else:
                decoded_connection.append(item)
        decoded_connections.append(decoded_connection)

    return decoded_connections




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
