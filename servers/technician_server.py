from datetime import timedelta
from fastapi import Response, encoders, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBasic
from fastapi import HTTPException, UploadFile, File, Body, Depends, APIRouter, Form
from starlette import status
import servers_implementation.file_db_actions as file_actions
from global_modules.Logger import logger
from servers_implementation import authorization, database_retrievals, database_adding
from issues import network, client, visit
from issues.network import Network
from servers_implementation import authentication

security = HTTPBasic()

IT4All_router = APIRouter()


@IT4All_router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    current_user = await authentication.authenticate_user(form_data.username, form_data.password)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=authorization.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    logger.info(f"{current_user} log in .")
    return {"access_token": access_token, "token_type": "bearer"}


@IT4All_router.post("/add_file/")
async def add_file(  # current_user: User = Depends(authorization.check_permission_of_technician),
        file: UploadFile = File(...),
        date_taken: str = Body(None),
        location_name: str = Body(None),
        network_name: str = Body(None)):
    # logger.info(f"{current_user} insert file.")
    if not date_taken or not location_name or not network_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not all requested data was provided")
    if client.current_client.client_id == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you need to send a client-id before you send this request.")
    network.current_network = Network(client_id=client.current_client.client_id, location=location_name,
                                      name=network_name)

    file_actions.check_the_file(file.filename)
    current_user_id = 4
    network_id = await file_actions.add_the_received_file_to_db(file)
    await database_adding.add_new_visit(network_id, current_user_id)
    return f"The file was received successfully.now you can get information about {network_id} network id"
