from fastapi import HTTPException, UploadFile, File, Body, Depends, APIRouter, Form
from fastapi.responses import FileResponse
from starlette import status
import servers_implementation.file_db_actions as file_actions
from global_modules.Logger import logger
from issues.client import ClientId
from servers_implementation import authorization, database_retrievals, database_adding
from issues import network, client, visit
from issues.network import Network
from issues.user import User, UserInDB

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


@IT4All_router.post("/add_file/")
async def add_file(  # current_user: User = Depends(authorization.check_permission_of_technician),
        file: UploadFile = File(...),
        date_taken: str = Body(None),
        location_name: str = Body(None),
        network_name: str = Body(None)):
    # logger.info(f"{current_user} insert file.")
    if not date_taken or not location_name or not network_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not all requested data was provided")
    if client.current_client.client_id == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you need to send a client-id before you send this request.")
    network.current_network = Network(client_id=client.current_client.client_id, location=location_name,
                                      name=network_name)

    file_actions.check_the_file(file.filename)
    current_user_id = 4
    network_id = await file_actions.add_the_received_file_to_db(file)
    await database_adding.add_new_visit(network_id, current_user_id)
    return f"The file was received successfully.now you can get information about {network_id} network id"


@IT4All_router.get("/get_client_by_id/{client_id}")
async def get_client_by_id(client_id):
    return await db_retrievals_implementation.get_client(client_id)


@IT4All_router.get(
    "/get_connections_in_network/{network_id}/")  # current_user: User = Depends(authorization.check_permission_of_technician))
async def get_connections_in_network(  # current_user: User = Depends(authorization.check_permission_of_technician),
        network_id):
    try:
        connections = await database_retrievals.get_connections_in_specific_network(network_id)
        print(connections)
    except Exception as e:
        print(e)
    else:
        if connections:
            view_graph = await database_retrievals.visualize_network_graph(connections)
            return FileResponse(view_graph)
        return "this network_id has no connections."


@IT4All_router.get("/get_devices_of_network_id/{network_id}")
async def get_devices_of_network_id(  # current_user: User = Depends(authorization.check_permission_of_technician),
        network_id):
    devices = await database_retrievals.get_lst_of_devices(network_id)
    if devices:
        return devices
    else:
        return "there is no devices"


@IT4All_router.get("/get_client_devices/{client_id}")
async def get_client_devices(  # current_user: User = Depends(authorization.check_permission_of_technician),
        client_id):
    devices = await db_additions_implementation.get_client_devices(client_id)
    if devices:
        return devices
    return "the client has no devices."


@IT4All_router.get("/device_protocols/{device_id}")
async def get_devices_protocols(  # current_user: User = Depends(authorization.check_permission_of_technician),
        device_id):
    protocols = await db_additions_implementation.get_device_protocols(device_id)
    if protocols:
        return protocols
    return "the macAddress devise has no protocols."


@IT4All_router.post("/add_report_about_the_network_id")
async def add_report_about_the_network_id(report: str = Body(...)):
    current_visit_id = visit.current_visit.visit_id
    try:
        await database_adding.add_report_to_the_current_visit(current_visit_id, report)
        return "thank you for your feedback!"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="error in the adding the report.")

# @IT4All_router.get("/get_reports_about_specific_network_id/{network_id}")
# async def get_reports_about_specific_network_id(network_id):
#
