from .ext_conn.sql_connector import SqlConnector

class UserX:
    """Representation of a database user account"""

    def __init__(self, user_name):
        self.user_name = user_name
        self.sql_conn = SqlConnector()

    def create_task(self, task_name, group_name, cube_id=None):
        """Creates a new task for the user"""
        self.sql_conn.create_task(self.user_name, task_name, group_name, cube_id)

    def delete_task(self, task_id):
        """Deletes a task from the user"""
        self.sql_conn.delete_task(task_id)

    def list_cubes(self):
        """Returns a list of all cubes assigned to the user"""
        return self.sql_conn.get_all_cube_id(self.user_name)

    def list_tasks(self, cube_id=None):
        """Returns a list of all the user's tasks"""
        return self.sql_conn.get_all_tasks(self.user_name, cube_id)

    def list_groups(self):
        """Returns a list of all the user's tasks"""
        return self.sql_conn.get_all_group_name(self.user_name)

def user_exists(telegram_id):
    """Checks if a telegram user's ID is already assigned to a database user account"""
    conn = SqlConnector()
    return conn.is_telegram_id_user(telegram_id)
