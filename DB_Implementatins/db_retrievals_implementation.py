from DB_Access import db_access
from issues.user import User, UserInDB


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


async def get_network_connections(network_id):
    select_communication_query = """
    SELECT C.Protocol,
      source_device.MacAddress as MacSource,
      source_device.Vendor as SourceVendor,
      destination_device.MacAddress as MacDestination,
      destination_device.Vendor as DestinationVendor
        FROM
            Connection C
        Join 
            Device source_device
        ON 
            C.Source=source_device.MacAddress
        Join
            Device destination_device
        ON 
            C.Destination=destination_device.MacAddress
        WHERE
            source_device.Network = %s
;"""
    val = network_id
    return await db_access.get_network_connections_from_db(select_communication_query, val)


async def get_devices_by_network_id(network_id):
    query = """SELECT Device.*, %s AS network_id 
                FROM Device 
                JOIN Network ON Device.Network = %s"""
    val = (network_id, network_id)
    devices = await db_access.get_multiple_data_from_db(query, val)
    if devices:
        return devices
    return None


get_devices_by_network_id(8)
