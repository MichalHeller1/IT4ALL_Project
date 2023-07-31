from tkinter import filedialog

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Body
from starlette import status
import controller.CRUD.file_actions as file_actions
from issuies import network
from issuies.network import Network

app = FastAPI()


@app.get("/")
def user():
    return "IT4All server is up!"


@app.post("/add_file/")
async def add_file(file: UploadFile = File(...), client_id: str = Body(None),
                   date_taken: str = Body(None),
                   location_name: str = Body(None),
                   network_name: str = Body(None)):
    if not client_id or not date_taken or not location_name or not network_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not all requested data was provided")
    # file_path = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap")])
    # from chavi daitch to add file with the full path of the file...
    network.current_network = Network(client_id=client_id, location=location_name, name=network_name)
    file_actions.check_the_file(file.filename)

    await file_actions.add_the_received_file_to_db(file.filename)
    return "The file was received successfully."


# @app.get("/get_connections_by_graph/{network_id}")
# async def get_connections_by_graph(network_id):



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
