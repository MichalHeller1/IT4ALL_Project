import uvicorn
from datetime import timedelta

from fastapi import FastAPI, Response, Depends, HTTPException, encoders, UploadFile, File, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, json
from starlette import status
import controller.CRUD.authorization as authorization
from controller.CRUD.user import User
import packets_file_system

IT4All_app = FastAPI()


@IT4All_app.get("/")
def user():
    return "IT4All server is up!"


@IT4All_app.post("/add_file/")
async def add_file(file: UploadFile = File(...), client_id: str = Body(...),
                   date_taken: str = Body(...),
                   location_name: str = Body(...)):
    if not packets_file_system.file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid pcap file."
        )
    else:
        # TODO: here we need to put the data baise with the detailes of the pcap file
        return {"filename": file.filename if file else None,
                "client_id": client_id if client_id else None,
                "date_taken": date_taken if date_taken else None,
                "location_name": location_name if location_name else None
                }


if __name__ == "__main__":
    uvicorn.run(IT4All_app, host="127.0.0.1", port=8000)
