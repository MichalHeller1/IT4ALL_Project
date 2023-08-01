from pydantic import BaseModel


class Connection(BaseModel):
    src_mac_address: str
    dst_mac_address: str
    protocol: str
