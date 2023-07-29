from pydantic import BaseModel


class Device(BaseModel):
    operation_system: str
    mac_address: str
    network_id: int


async def create_new_device(os: str, macAddress: str, networkId: int):
    new_device = Device(operation_system=os, mac_address=macAddress, network_id=int(networkId))
    return new_device
