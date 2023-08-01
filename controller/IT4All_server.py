import os
import sys
# to make sys search from network_analyst not from my_api
curr_path = os.path.dirname(__file__)
root_path = os.path.join(curr_path, "..")
sys.path.append(root_path)

print(sys.path)
from tkinter import filedialog

import uvicorn
from datetime import timedelta
from fastapi import FastAPI, Response, Depends, HTTPException, encoders, UploadFile, File, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, json
from starlette import status
import CRUD.file_actions as file_actions
from issuies.network import Network

from DB_Implementatins import db_implementation

IT4All_app = FastAPI()


@IT4All_app.get("/")
def user():
    return "IT4All server is up!"


@IT4All_app.get("/get_connections_in_network/network_id")
async def get_connections_in_network(network_id):
    connections = await db_implementation.get_network_connections(network_id)
    return connections


@IT4All_app.post("/add_file/")
async def add_file(file: UploadFile = File(...), client_id: str = Body(None),
                   date_taken: str = Body(None),
                   location_name: str = Body(None),
                   network_name: str = Body(None)):
    if not client_id or not date_taken or not location_name or not network_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not all requested data was provided")
    # from chavi daitch to add file with the full path of the file...
    # file_path = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap")])
    Network.client_id = client_id
    Network.location = location_name
    Network.name = network_name
    file_actions.check_the_file(file.filename)

    await file_actions.add_the_received_file_to_db(file.filename)
    return "The file was received successfully."

if __name__ == "__main__":
    uvicorn.run(IT4All_app, host="127.0.0.1", port=8000)
