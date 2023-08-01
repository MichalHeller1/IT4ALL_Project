import pymysql
from fastapi import Depends
from pymysql import IntegrityError
# from controller.CRUD.user import UserInDB

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
        query = """INSERT INTO Device (MacAddress, Vendor, Network) 
                        VALUES (%s, %s, %s) 
                        ON DUPLICATE KEY UPDATE Vendor=VALUES(Vendor), Network=VALUES(Network)"""

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


async def get_network_connections(network_id):
    print("i am i the get_network_connections func")
    select_communication_query = """
    SELECT C.Protocol,
      source_device.MacAddress as MacSource,
      source_device.Vendor as SourceVendor,
      destination_device.MacAddress as MacDestination,
      destination_device.Vendor as DestinationVendor
FROM Connection C
Join Device source_device
ON C.Source=source_device.MacAddress
Join Device destination_device
ON C.Destination=destination_device.MacAddress
WHERE source_device.Network = %s
;"""
    val = network_id
    return await db_access.get_network_connections_from_db(select_communication_query, val)


async def get_client_devices(client_id):
    query = """SELECT Device.MacAddress, Device.Vendor, Device.Network FROM Device
        JOIN Network
        On Device.Network=Network.id
        WHERE Network.Client=%s
        """
    val = client_id
    devices = await db_access.get_client_devices_from_db(query, val)
    return [Device(mac_address=device[0], vendor=device[1], network_id=device[2]) for device in devices]


async def get_device_protocols(mac_address):
    query = """SELECT Protocol
    FROM Connection
    WHERE Source=%s OR Destination=%s
    GROUP BY Protocol
    """
    val = mac_address, mac_address
    return await db_access.invoke_query(query, val)

