from pydantic import BaseModel


class ClientId(BaseModel):
    client_id: int = None


current_client_id = ClientId()
