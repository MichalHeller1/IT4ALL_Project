from fastapi import HTTPException, Depends
from starlette import status

import DB_Implementatins.db_implementation as db_implementation

import packets_file_system
from issuies import network, device
from issuies.network import NetworkInDB, Network


def check_the_file(file):
    # ask the teacher where exactly the try and the catch need to be.
    # here or in the db_implementation or db_access or both of them?
    if not packets_file_system.check_file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid pcap file."
        )


async def add_network():
    try:
        new_network = network.current_network
        new_network_id = await db_implementation.add_new_network(new_network)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The request rejected. Invalid data provided."
        )
    return new_network_id


async def add_devices_from_pcap_file(pcap_file):
    devices_to_add = await packets_file_system.get_devices_to_add(pcap_file)
    await db_implementation.add_devices(devices_to_add)


async def add_the_received_file_to_db(file):
    network_id = await add_network()
    network.current_network = NetworkInDB(**network.current_network.dict(), network_id=network_id)
    await add_devices_from_pcap_file(file)
