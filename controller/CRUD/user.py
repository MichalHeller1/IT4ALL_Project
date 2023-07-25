from typing import Union

import app as app
import uvicorn
from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    username: constr(min_length=3)
    email: Union[EmailStr, None] = None
    password: constr(min_length=5) = ""
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


# new_user = User(user_name="tovi", email="t0583232818@gmail.com", password="f5ef8", disabled=True)
# print(new_user)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
