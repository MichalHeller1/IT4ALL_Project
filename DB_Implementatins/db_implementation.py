import pymysql
from fastapi import Depends
from pymysql import IntegrityError

from DB_Access.db_access import get_network_connections_from_db
from issues.user import UserInDB, User
from DB_Access import db_access
from issues.connection import Connection, DevicesConnection
from issues.device import Device
from issues.network import Network, current_network


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


async def check_permission(user: User, client_id):
    query = """
                SELECT Technician.id
                FROM Technician
                JOIN Permissions ON Technician.id = Permissions.Technician
                JOIN Client ON Permissions.Client = Client.id
                WHERE Technician.Name = %s AND Client.id = %s
            """
    val = (user.username, client_id)
    permission = bool(db_access.get_data_from_db(query, val))
    return permission


async def get_network_connections(network_id):
    print(network_id)
    query = """
          SELECT 
    conn.id AS connection_id,
    conn.Protocol,
    dev1.MacAddress AS source_mac_address,
    dev1.Vendor AS source_provider,
    net1.Name AS source_network_name,
    dev2.MacAddress AS destination_mac_address,
    dev2.Vendor AS destination_provider,
    net2.Name AS destination_network_name
FROM 
    Connection conn
JOIN 
    Device dev1 ON conn.Source = dev1.MacAddress
JOIN 
    Device dev2 ON conn.Destination = dev2.MacAddress
JOIN
    Network net1 ON dev1.Network = net1.id
JOIN
    Network net2 ON dev2.Network = net2.id
WHERE 
    net1.id = %s
    AND net2.id = %s

          """
    val = (network_id, network_id)
    decoded_connections = await get_network_connections_from_db(query, val)
    full_connections = []

    for connection in decoded_connections:
        mac_address1 = connection[2]
        vendor1 = connection[3]
        network_id1 = 1

        mac_address2 = connection[5]
        vendor2 = connection[6]
        network_id2 = 1

        device1 = Device(vendor=vendor1, mac_address=mac_address1, network_id=network_id1)
        device2 = Device(vendor=vendor2, mac_address=mac_address2, network_id=network_id2)

        full_connection = DevicesConnection(src_device=device1, dst_device=device2, protocol=connection[1])
        full_connections.append(full_connection)

    return full_connections

    # return db_access.get_network_connections_from_db(query, val)
