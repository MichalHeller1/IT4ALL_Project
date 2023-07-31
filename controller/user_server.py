import uvicorn
from datetime import timedelta
import app
from fastapi import FastAPI, Response, Depends, HTTPException, encoders, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
import controller.CRUD.authorization as authorization

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

security = HTTPBasic()

user_app = FastAPI()


@user_app.get("/user")
def user():
    return "user"


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "johnsmith") or not (credentials.password == "swordfish"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/profile")
async def main(username: str = Depends(get_current_username)):
    return {"username": username}


@user_app.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    current_user = await authorization.authenticate_user(form_data.username, form_data.password)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=authorization.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authorization.create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(user_app, host="127.0.0.1", port=8000)
