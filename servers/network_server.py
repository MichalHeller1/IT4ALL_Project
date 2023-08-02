from fastapi import HTTPException, UploadFile, File, Body, Depends, APIRouter, Form
from fastapi.responses import FileResponse
from starlette import status
from servers_implementation import authorization, database_retrievals, database_adding
from issues import network, client, visit
IT4All_router = APIRouter()

@IT4All_router.get("/get_connections_in_network/{network_id}/")
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


@IT4All_router.post("/add_report_about_the_network_id")
async def add_report_about_the_network_id(report: str = Body(...)):
    print(report)
    current_visit_id = visit.current_visit.visit_id
    try:
        await database_adding.add_report_to_the_current_visit(current_visit_id, report)
        return "thank you for your feedback!"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="error in the adding the report.")
