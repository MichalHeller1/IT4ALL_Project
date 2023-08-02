import uvicorn
from fastapi import FastAPI
from servers.IT4All_server import IT4All_router
from servers.user_server import user_router
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

app.include_router(IT4All_router)
app.include_router(user_router)

@app.get("/")
async def root():
    # database_retrievals.visualize_network_graph(database_retrievals.connections)
    return "the app is running..."


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
