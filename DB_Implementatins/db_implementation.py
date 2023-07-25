from controller.CRUD.user import UserInDB
from DB_Access import db_access


async def get_user_from_db(user_name):
    # TODO:get the user from the sql DB
    user = db_access.get_user(user_name)
    if user:
        return UserInDB(**user)
