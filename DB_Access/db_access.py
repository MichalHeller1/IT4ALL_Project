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
    print("i am in the get_network_connections_from_db func")
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

    print("got all connections")
    return decoded_connections


