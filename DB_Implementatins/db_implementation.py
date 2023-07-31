from pymysql import IntegrityError

from issuies.user import UserInDB
from DB_Access import db_access
from issuies.connection import Connection
from issuies.device import Device
from issuies.network import Network


async def get_user_from_db(user_name):
    query = """SELECT * FROM Technician WHERE Name = %s"""
    val = user_name
    user = await db_access.get_data_from_db(query, val)
    if user:
        return UserInDB(**user)


# async def insert_new_network2(new_network: Network = Depends(create_new_network())):
#     print( f"network added.{new_network}")

async def add_new_network(network: Network):
    try:
        query = """INSERT into Network (Name,Location,Client)
                            values (%s, %s, %s)"""
        val = (network.name, network.location, network.client_id)
        network_id = await db_access.add_new_data_to_db(query, val)
    except IntegrityError as e:
        raise e
    else:
        return network_id


async def add_device(device: Device):
    try:
        query = """INSERT IGNORE into Device (MacAddress,Provider,Network) 
                                    values (%s, %s, %s)"""
        val = (device.mac_address, device.vendor, device.network_id)
        device_id = await db_access.add_new_data_to_db(query, val)
    except IntegrityError as e:
        raise e
    else:
        return device_id


async def add_connection(connection: Connection):
    try:
        query = """INSERT into Connection (Protocol,Source,Destination)
                                      values (%s, %s, %s)"""
        val = (connection.protocol, connection.src_mac_address, connection.dst_mac_address)
        device_id = await db_access.add_new_data_to_db(query, val)
    except IntegrityError as e:
        raise e
    else:
        return device_id


async def add_devices(devices: dict):
    for value in devices.values():
        await add_device(value["device"])
    for value in devices.values():
        for connection in value["connections"]:
            await add_connection(connection)
