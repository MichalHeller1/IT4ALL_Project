from controller.CRUD.user_data_base import users_db


def get_user(user_name):
    return users_db.get(user_name)
