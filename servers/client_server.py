from fastapi import HTTPException, APIRouter, Form
from servers_implementation import authorization, database_retrievals, database_adding
from DB_Implementatins import db_additions_implementation, db_retrievals_implementation

IT4All_router = APIRouter()


@IT4All_router.post("/send_client_id")
async def get_client_id(client_id: str = Form(...)):
    c_id = int(client_id)
    current_client = await database_retrievals.check_client_id_in_db(c_id)
    if current_client:
        return f"ok.now you can do your actions to get or post to this client." \
               f"the client you work with is:{current_client}"
    else:
        return "there is no client with this id."


@IT4All_router.get("/get_client_by_id/{client_id}")
async def get_client_by_id(client_id):
    return await db_retrievals_implementation.get_client(client_id)


@IT4All_router.get("/get_client_devices/{client_id}")
async def get_client_devices(  # current_user: User = Depends(authorization.check_permission_of_technician),
        client_id):
    devices = await db_additions_implementation.get_client_devices(client_id)
    if devices:
        return devices
    return "the client has no devices."
