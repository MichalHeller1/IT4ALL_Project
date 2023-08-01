import uvicorn
from fastapi import FastAPI
from controller.user_server import user_app

app = FastAPI()

@app.get("/")
async def root():
    return "the app is running..."


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
