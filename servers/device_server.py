from fastapi import HTTPException, APIRouter, Form
from DB_Implementatins import db_additions_implementation, db_retrievals_implementation

IT4All_router = APIRouter()


@IT4All_router.get("/device_protocols/{device_id}")
async def get_devices_protocols(  # current_user: User = Depends(authorization.check_permission_of_technician),
        device_id):
    protocols = await db_additions_implementation.get_device_protocols(device_id)
    if protocols:
        return protocols
    return "the macAddress devise has no protocols."

# @IT4All_router.get("/get_reports_about_specific_network_id/{network_id}")
# async def get_reports_about_specific_network_id(network_id):
#
