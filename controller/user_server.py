import uvicorn
from datetime import timedelta
from fastapi import  Response, Depends, HTTPException, encoders, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
import controller.CRUD.authentication as authorization

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

from app import logger

security = HTTPBasic()

user_router = APIRouter()


@user_router.get("/user")
def user():
    return "user"


@user_router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    current_user = await authorization.authenticate_user(form_data.username, form_data.password)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=authorization.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authorization.create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    logger.info(f"{current_user} log in .")
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(user_router, host="127.0.0.1", port=8000)
