import uvicorn
from fastapi import FastAPI
from servers.device_server import IT4All_router as device
from servers.technician_server import IT4All_router as technician
from servers.client_server import IT4All_router as client
from servers.network_server import IT4All_router as network

from servers_implementation import database_retrievals
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "null",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device)
app.include_router(technician)
app.include_router(client)
app.include_router(network)



@app.get("/")
async def root():
    # database_retrievals.visualize_network_graph(database_retrievals.connections)
    return "the app is running..."


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
