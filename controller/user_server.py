from fastapi import FastAPI

user_app = FastAPI()


@user_app.get("/user")
def user():
    return "user"
