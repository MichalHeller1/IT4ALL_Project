from fastapi import HTTPException, UploadFile, File, Body, Depends, APIRouter, Form
from fastapi.responses import FileResponse
from starlette import status
import servers_implementation.file_actions as file_actions
from global_modules.Logger import logger
from issues.client import ClientId
from servers_implementation import authorization, database_retrievals
from issues import network, client
from issues.network import Network
from issues.user import User

from DB_Implementatins import db_additions_implementation, db_retrievals_implementation


IT4All_router = APIRouter()


@IT4All_router.get("/get_connections_in_network/{network_id}/")
async def get_connections_in_network(network_id,
                                     current_user: User = Depends(authorization.check_permission_of_technician)):
    try:
        connections = await database_retrievals.get_connections_in_specific_network(network_id)
        print(connections)
    except Exception as e:

        print(e)

    else:
        if connections:
            view_graph = database_retrievals.visualize_network_graph(connections)
            return FileResponse(view_graph)
    return "this network_id has no connections."


@IT4All_router.get("/get_connections_in_network/{network_id}")
async def get_connections_in_network(network_id):
    connections = await db_retrievals_implementation.get_network_connections(network_id)
    return connections


@IT4All_router.post("/send_client_id")
async def get_client_id(client_id: str = Form(None)):
    ci = int(client_id)
    client.current_client_id = ClientId(client_id=ci)
    return "ok.now you can do your actions to get or post to this client."



@IT4All_router.get("/get_client_devices/{client_id}")
async def get_client_devices(client_id):
    devices = await db_additions_implementation.get_client_devices(client_id)
    return devices


@IT4All_router.get("/device_protocols/{device_id}")
async def get_devices_protocols(device_id):
    protocols = await db_additions_implementation.get_device_protocols(device_id)
    return protocols


@IT4All_router.post("/add_file/")
async def add_file(current_user: User = Depends(authorization.check_permission_of_technician),
                   file: UploadFile = File(...),
                   date_taken: str = Body(None),
                   location_name: str = Body(None),
                   network_name: str = Body(None)):
    logger.info(f"{current_user} insert file.")
    if not client.current_client_id.client_id or not date_taken or not location_name or not network_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not all requested data was provided")
    network.current_network = Network(client_id=client.current_client_id.client_id, location=location_name,
                                      name=network_name)
    file_actions.check_the_file(file.filename)

    network_id = await file_actions.add_the_received_file_to_db(file)
    return f"The file was received successfully.now you can get information about {network_id} network id"

# @app.get("/get_connections_by_graph/{network_id}")
# async def get_connections_by_graph(network_id):
