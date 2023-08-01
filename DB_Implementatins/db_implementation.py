from pymysql import IntegrityError

from issuies.user import UserInDB, User
from DB_Access import db_access
from issuies.connection import Connection
from issuies.device import Device
from issuies.network import Network


async def get_user_from_db(user_name):
    query = """SELECT * FROM Technician WHERE Name = %s"""
    val = user_name
    user = await db_access.get_data_from_db(query, val)

    if user:
        name = user[1]
        password = user[2]
        phone = user[3]
        email = user[4]
    if user:
        return User(username=name, password=password, phone=phone, email=email)


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
        query = query = """INSERT INTO Device (MacAddress, Provider, Network) 
                        VALUES (%s, %s, %s) 
                        ON DUPLICATE KEY UPDATE Provider=VALUES(Provider), Network=VALUES(Network)"""

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


async def add_technician(user: User):
    query = """
        INSERT INTO Technician(
        Name,Password,Phone,Email
        )
        values(%s,%s,%s,%s)
    """
    val = (user.username, user.password, user.phone, user.email)
    await db_access.add_new_data_to_db(query, val)


async def check_permission(user: User):
    # query = """
    #         ...
    #     """
    # val = (user.username, user.password, user.phone, user.email)
    # await db_access.add_new_data_to_db(query, val)
    return True
