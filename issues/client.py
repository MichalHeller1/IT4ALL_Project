from pydantic import BaseModel


class ClientId(BaseModel):
    client_id: int = None


class Client(ClientId):
    name: str = None
    address: str = None
    phone: str = None
    email: str = None


current_client_id = ClientId()
