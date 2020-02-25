from sql.sql_Connector import SqlConn

class UserX:

    def __init__(self, user_name):
        self.user_name = user_name
        self.sql_conn = SqlConn() 

    def create_task(self, task_name, group_name, cube_id):
        self.sql_conn.create_task(self.user_name, cube_id, task_name, group_name)

    def delete_task(self, task_id):
        self.sql_conn.delete_task(self.user_name, task_id)

    def list_cubes(self):
        return self.sql_conn.get_all_cube_id(self.user_name)

    def list_tasks(self, cube_id):
        return self.sql_conn.get_all_tasks(self.user_name, cube_id)

    def list_groups(self):
        return self.sql_conn.get_all_group_name(self.user_name)

def telegram_to_user(telegram_id, user_name):
    pass

def create_user(name, password):
    pass