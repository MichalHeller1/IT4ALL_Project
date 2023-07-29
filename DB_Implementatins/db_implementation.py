import pymysql
from fastapi import Depends
from pymysql import IntegrityError

from controller.CRUD.user import UserInDB
from DB_Access import db_access
from issuies.device import Device
from issuies.network import Network


async def get_user_from_db(user_name):
    # TODO:get the user from the sql DB
    user = db_access.get_user(user_name)
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
        # print(f"error: {e}")
        raise e
    else:
        print("ok from add network.")
        return network_id


async def add_new_device(device: Device):
    try:
        query = """INSERT into Device (OS,MacAddress,Network)
                                    values (%s, %s, %s)"""
        val = (device.operation_system, device.mac_address, device.network_id)
        device_id = await db_access.add_new_data_to_db(query, val)
    except IntegrityError as e:
        # print(f"error: {e}")
        raise e
    else:
        print("ok from add device.")
        return device_id

