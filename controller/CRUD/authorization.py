from fastapi import FastAPI
from app import app

app_user = FastAPI()
app.include_router(app)


@app_user.get("/app_userer")
async def user_func():
    return "hello i am user"
