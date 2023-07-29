from pydantic import BaseModel


class Network(BaseModel):
    name: str = None
    location: str = None
    client_id: int = None


class NetworkInDB(Network):
    network_id: int = None


async def create_new_network():
    new_network = Network()
    return new_network
