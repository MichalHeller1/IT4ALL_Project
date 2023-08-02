from pydantic import BaseModel


class Visit(BaseModel):
    visit_id: int = None,
    technician_id: int = None,
    network_id: int = None


current_visit = Visit()
