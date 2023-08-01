from pydantic import BaseModel


class Device(BaseModel):
    vendor: str
    mac_address: str
    network_id: int



