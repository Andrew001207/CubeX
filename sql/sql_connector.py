#!/usr/bin/env python3
"""
Created on Thu Feb 13 12:50:37 2020

@author: matthiasmoser
"""
import base64
from sqlite3 import OperationalError

import json
import logging
import traceback
import psycopg2
import hashlib

from config_aware import ConfigAware

logger = logging.getLogger("sqlconnector")
logger.setLevel(logging.WARNING)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

class SqlConnector(ConfigAware):
    '''
    Connection to database
    Methods for interacting with the database

    :param configdict: database connection information
    '''

    def make_conn(self):
        params = self.conf_db
        try:
            return psycopg2.connect(**params)
        except:
            raise Exception('connection could not be established. Maybe because of bad credentials.')


    def fetch_data(self, cmd):
        """
        fetches data from the aws server

        :param cmd: sql command in string format
        :return: the requested data as list of touple
        """
        if "select" not in cmd:
            logger.warning("tryed to fetch data with \
                        a cmd that return nothing")
            return None

        conn = self.make_conn()
        result = []
        logger.info("Now executing: %s" % (cmd))
        cursor = conn.cursor()
        cursor.execute(cmd)
        raw = cursor.fetchall()
        #TODO Schleife notwendig?
        for line in raw:
            result.append(line)
        cursor.close()
        conn.close()
        return result


    def execute_command(self, cmd):
        """
        executes sql cmd on the aws server

        :param cmd: sql cmd in string format
        :return: nothing
        """
        conn = self.make_conn()
        cursor = conn.cursor()
        logger.info("Now executing: %s" % (cmd))
        cursor.execute(cmd)
        conn.commit()
        cursor.close()
        conn.close()


    def _execute_Scripts_From_File(self, filename):
        """
        executes sql scrips from file

        :param filename: filename of sql script
        :return:
        """
        # Open and read the file as a single buffer
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        # Execute every command from the input file
        for command in sqlCommands:
            try:
                print(command)
# TODO why is here a print?
                self.execute_command(command)
            except OperationalError as msg:
                print("Command skipped: ", msg)
# TODO why is here a print?


    def create_task_from_json(self,cube_id, file_path):
        """
        takes the json file and creates all task that are in it

        :param json_file: json_file
        :return:
        """
        username = "Paula"
        with open(file_path) as json_file:
            data = json.load(json_file)
            for group in data['groups']:
                for task in data[group]['tasks']:
                    self.create_task(username,cube_id, task, group)


    def create_task(self, username, task_name, group_name, cube_id=None,):
        """
        creates task on the aws database

        :param cube_id: integer
        :param task_name: string
        :param group_name: string
        :return: none
        """
        if cube_id is None:
            try:
                self.execute_command("insert into task values (default,'{}','{}', null, '{}');".format(task_name, group_name,username))
            except:
                print(traceback.format_exc())
# TODO why is here a print?
                logger.warning("task schon vorhanden")
        else:
            try:
                self.execute_command("insert into task values (default,'{}','{}', {}, '{}');".format(task_name, group_name, cube_id, username))
            except:
                print("1",traceback.format_exc())
# TODO why is here a print?
                logger.warning("task schon vorhanden")



    def create_cube(self,cube_id):
        """
        creates cube on the aws database

        :param cube_id: integer
        :return:
        """
        username = "Paula"
        self.execute_command("insert into cube values ({},'{}');".format(cube_id,username))


    def set_task(self, cube_id, side_id, task_id):
        """
        :param cube_id: integer
        :param side_id: integer
        :param task_name: string
        :param group_name: string
        :return: nothing
        """
        #creates and sets tasks if wanted
        #create_task(cube_id ,task_name, group_name)

        try:
            self.execute_command("insert into side values ({},{},{});".format(side_id, cube_id, task_id))
        except:
            self.execute_command("update side set Task_Id = {} where side_id = {} and cube_id = {};" \
                            .format(task_id, side_id, cube_id))


    def delete_task(self, task_id):
        """

        :param cube_id: integer
        :param task_id: int
        :return: nothing
        """
        self.execute_command(
            "delete from task where task_id = {};".format(task_id))

    def check_cube(self, cube_id):
        """"
        checks if cube is aready existent

        """
        check = False
        data = self.fetch_data("select * from cube where cube_id = {}".format(cube_id))
        for cube in data:
            if cube_id in cube:
                check = True
        return check

    def write_cube_information_json(self, cube_id):
        """
        writes all information about the cubes tasks and events

        :param cube_id: integer
        :return: data
        """
        #all the tasks,
        groups = self.fetch_data("select distinct group_name from task where cube_id = {};".format(cube_id))
        tasks = self.fetch_data("select * from task where cube_id = {};".format(cube_id))
        events = self.fetch_data("select * from event where cube_id = {};".format(cube_id))
        data = {}
        data['groups'] = []
        for group in groups:
            data['groups'].append(group[0])
            data[group[0]] = []
        for task in tasks:
            data[task[1]].append(task[0])
        data['events'] = []
        for event in events:
            data['events'].append([event[1], event[2], event[4], event[5]])
        return data

    def write_cube_state_json(self, cube_id):
        """
        writes the information about the cube state 

        :param cube_id: integer
        :return: data
        """
        sides = self.fetch_data("select * from side where Cube_ID = {}".format(cube_id))
        data = {}
        data['side'] = []
        for side in sides:
            task = self.fetch_data("select Task_Name from task where Task_Id = {};".format(side[2]))
            group = self.fetch_data("select Group_name from task where Task_Id = {};".format(side[2]))
            data['side'].append(
                {
                    'side': side[0],
                    'cube_id': side[1],
                    'task': task[0][0],
                    'group': group[0][0]

                }
            )
        return data


    def fetch_to_list(self, data):
        """
        convertes the fetch_data result into a list (1 column)

        :param data: Bytes
        :return: liste
        """
        liste = list()
        for part in data:
            liste.append(part[0])
        return liste

    def fetch_multiple_to_list(self, data):
        """
        convertes the fetch_data result into a list (multiple columns)

        :param data: Bytes
        :return: liste
        """
        liste = list()
        for part in data:
            liste.append(part)
        return liste

    def get_side_info(self,cubeid):
        """
        Returns sideid, task_name and group_name for every side

        :param cubeid: integer
        :return: list
        """
        sides = self.fetch_data("select s.side_id, t.task_name, t.group_name from side s INNER JOIN task t ON s.task_id = t.task_id where s.Cube_ID = {};".format(cubeid))
        return self.fetch_multiple_to_list(sides)     

    def get_all_tasks(self, username, cubeid):
        """
        Returns all tasks for a specific user and cube

        :param username: String
        :param cubeid: Integer
        :return: liste
        """
        if cubeid:
            return self.fetch_multiple_to_list(self.fetch_data("select task_id,task_name,group_name from task where username = '{}' and (cube_id = {} or cube_id is null);".format(username,cubeid)))
        else:
            return self.fetch_multiple_to_list(self.fetch_data("select task_id,task_name,group_name from task where username = '{}';".format(username)))

    def get_all_group_name(self, username):
        """
        Returns all groups for a specific user

        :param username: String
        :return: liste
        """
        return self.fetch_to_list(self.fetch_data("select distinct Group_name from Task where username = '{}';".format(username)))

    def get_all_cube_id(self, username):
        """
        Returns all cubes for a specific user

        :param username: String
        :return: liste
        """
        return self.fetch_to_list(self.fetch_data("select cube_ID from cube where username = '{}'".format(username)))

    def set_telegram_user(self, username, telegram_id):
        """
        creates a user for a telegram_user 

        :param username: String
        :param telegram_username: String
        :return: none
        """
        self.execute_command("update auth_user set telegram_id = {} where username = {}".format(telegram_id,username))

    def update_event(self, task_name, cube_id):
        """
        gets called when the cube changes its state. Setting the end time of the old event, creating a new event
        with a start time

        :param task_name: String
        :param cubeid: Integer
        :return: none
        """
    # Group_ID wird ignoriert
        username = self.fetch_data("select username from cube where Cube_ID = {};".format(cube_id))[0][0]
        task_id = self.fetch_data("select Task_Id from task where username = '{}' and Task_Name = '{}';".format(username,task_name))[0][0]

        self.execute_command("update event set end_time = clock_timestamp() where start_time = (select max(start_time) from event);")
        self.execute_command("insert into event values (default, {}, clock_timestamp(), null );".format(task_id))

    def is_telegram_id_user(self, telegram_id):
        """
        checkes if the telegram_id is connected to a user

        :param telegram_id: String
        :return: boolean
        """
        list = self.fetch_to_list(self.fetch_data("select username from auth_user where telegram_id = {}".format(telegram_id)))
        if len(list) == 0:
            return False
        else:
            return True

    def signup_user(self, username, password, telegram_id = None, first_name = "",last_name = "",email = "", is_staff = False, is_active = True):
        """
        sets a user in auth_user

        :return: none
        """
        password_hash = self.create_pw_hash(password)
        self.execute_command(
            f"insert into auth_user(username, password, telegram_id, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined) VALUES ('{username}','{password_hash}','{telegram_id}', FALSE,'{first_name}','{last_name}','{email}','{is_staff}','{is_active}', clock_timestamp() )")

    def pbkdf2(self, password, salt, iterations, dklen=0, digest=None):
        """Return the hash of password using pbkdf2."""
        if digest is None:
            digest = hashlib.sha256
        dklen = dklen or None
        password = password.encode()
        salt = salt.encode()
        return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)

    def compare_pw(self, pw, username):
        """compares the given password with the user."""
        hashed_pw = self.fetch_to_list(self.fetch_data("select password from auth_user where username = '{}'".format(username)))
        hash_string = hashed_pw[0]
        args = hash_string.split('$')
        compare_hash = self.hash_pw(args, pw)
        compare_hash = base64.b64encode(compare_hash).decode('ascii').strip()
        if compare_hash == args[3]:
            return True
        else:
            return False

    def encode(self, password, salt, algorithm, iterations=None):
        """encodes the password"""
        assert password is not None
        assert salt and '$' not in salt
        iterations = iterations or iterations
        hash = self.pbkdf2(password, salt, iterations)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (algorithm, iterations, salt, hash)

    def salt(self):
        """creates a random salt"""
        import random
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars = []
        for _ in range(16):
            chars.append(random.choice(alphabet))
        salt = "".join(chars)
        return salt

    def hash_pw(self, args, pw):
        """hashes the password"""
        hashed_pw = hashlib.pbkdf2_hmac('sha256', pw.encode(), args[2].encode(), int(args[1]))
        return hashed_pw

    def create_pw_hash(self, pw):
        """creates a password hash"""
        return self.encode(pw, self.salt(), 'pbkdf2_sha256', 150000)

