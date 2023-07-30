import os
from tkinter import filedialog

import uvicorn
from datetime import timedelta
from DB_Implementatins import db_implementation
from fastapi import FastAPI, Response, Depends, HTTPException, encoders, UploadFile, File, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, json
from starlette import status
import controller.CRUD.authorization as authorization
import controller.CRUD.file_actions as file_actions
from controller.CRUD.user import User
import packets_file_system
from issuies import network
from DB_Implementatins.db_implementation import add_new_network
from issuies.network import Network

IT4All_app = FastAPI()


@IT4All_app.get("/")
def user():
    return "IT4All server is up!"


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
