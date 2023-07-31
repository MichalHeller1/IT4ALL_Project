from datetime import datetime, timedelta
from typing import Union
from jose import jwt
from passlib.context import CryptContext
from DB_Implementatins import db_implementation
from issuies.user import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "6hFiwU20LvHCMcZZlDiExQE_n9sSyyBomFiltXrxF9c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(user_name: str, password: str):
    user: UserInDB = await db_implementation.get_user_from_db(user_name)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
