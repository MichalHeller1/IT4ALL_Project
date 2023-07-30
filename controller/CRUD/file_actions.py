from fastapi import HTTPException, Depends
from starlette import status

import DB_Implementatins.db_implementation as db_implementation

import packets_file_system
from issuies import network, device
from issuies.network import NetworkInDB


def check_the_file(file):
    # ask the teacher where exactly the try and the catch need to be.
    # here or in the db_implementation or db_access or both of them?
    if not packets_file_system.file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid pcap file."
        )


# new_network: Network = Depends(network.create_new_network)
async def get_network():
    # new_network = await create_new_network()
    try:
        new_network = await network.create_new_network()
        new_network_id = await db_implementation.add_new_network(new_network)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The request rejected. Invalid data provided."
        )
    return new_network_id


async def add_devices_from_the_file(file):
    mac_addresses_lst = await packets_file_system.get_mac_addresses_from_pcap(file)
    # TODO: here is going to be a function that take every mac address and add it to the db=to the device table
    for mac in mac_addresses_lst:
        try:
            new_device = await device.create_new_device("o-s", mac, NetworkInDB.network_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The request rejected. Invalid data provided."
            )
        await db_implementation.add_new_device(new_device)


async def add_the_received_file_to_db(file, network_id: int = Depends(get_network)):
    NetworkInDB.network_id = await get_network()

    await add_devices_from_the_file(file)
