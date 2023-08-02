import asyncio

from DB_Access.DB_connection import connection


# async def get_network_connections_from_db(query, val):
#     with connection.cursor() as cursor:
#         cursor.execute(query, val)
#         connection.commit()
#         connections_in_network = cursor.fetchall()
#     print("got all connections")
#     return connections_in_network


async def invoke_query(query, val):
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
        db_result = cursor.fetchall()
    return db_result


async def get_network_connections(network_id):
    get_source_query = """SELECT * FROM Device 
                WHERE Device.MacAddress IN (SELECT Source FROM Connection) 
                AND Device.Network = %s"""

    get_destination_query = """SELECT * FROM Device 
                WHERE Device.MacAddress IN (SELECT Destination FROM Connection) 
                AND Device.Network = %s"""
    val = network_id
    sources = await invoke_query(get_source_query, val)
    destinations = await invoke_query(get_destination_query, val)
    return sources, destinations


def get_communication(network_id):
    select_communication_query = """
    SELECT C.Protocol,
      source_device.MacAddress as MacSource,
      source_device.Provider as SourceProvider,
      source_device.Network,
      destination_device.MacAddress as MacDestination,
      destination_device.Provider as DestinationProvider
FROM Connection C
Join Device source_device
ON C.Source=source_device.MacAddress
Join Device destination_device
ON C.Destination=destination_device.MacAddress
WHERE source_device.Network = %s
;"""
    val = network_id
    return invoke_query(select_communication_query, val)


async def main():
    result = await get_communication(82)
    print(result)


def get_devices_by_client(client_id):
    query = """SELECT * FROM Device
    Join Network
    On Device.Network=Network.id
    WHERE Network.Client=%s
    """

asyncio.run(main())

