import uvicorn
from fastapi import FastAPI
from controller.IT4All_server import IT4All_router
from controller.user_server import user_router


app = FastAPI()

app.include_router(IT4All_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return "the app is running..."


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
