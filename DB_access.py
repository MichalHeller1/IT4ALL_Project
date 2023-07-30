from controller.CRUD.user_data_base import users_db


class DB_Access:
    @classmethod
    def get_user(self,user_name):
        return users_db.get(user_name)