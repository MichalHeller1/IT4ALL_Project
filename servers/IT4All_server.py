from fastapi import  HTTPException, UploadFile, File, Body, Depends, APIRouter
from starlette import status
import servers_implementation.file_actions as file_actions
from global_modules.Logger import logger
from servers_implementation import authorization
from issuies import network
from issuies.network import Network
from issuies.user import User

from DB_Implementatins import db_implementation


IT4All_router = APIRouter()





@IT4All_router.get("/get_connections_in_network/network_id")
async def get_connections_in_network(network_id):
    connections = await db_implementation.get_network_connections(network_id)
    return connections

@IT4All_router.post("/add_file/")
async def add_file(current_user: User = Depends(authorization.check_permission_of_technician),
                   file: UploadFile = File(...),
                   client_id: str = Body(None),
                   date_taken: str = Body(None),
                   location_name: str = Body(None),
                   network_name: str = Body(None)):
    logger.info(f"{current_user} insert file.")
    if not client_id or not date_taken or not location_name or not network_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not all requested data was provided")
    network.current_network = Network(client_id=client_id, location=location_name, name=network_name)
    file_actions.check_the_file(file.filename)

    await file_actions.add_the_received_file_to_db(file)
    return "The file was received successfully."


# @app.get("/get_connections_by_graph/{network_id}")
# async def get_connections_by_graph(network_id):

