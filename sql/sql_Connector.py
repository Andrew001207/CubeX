#!/usr/bin/env python3
"""
Created on Thu Feb 13 12:50:37 2020

@author: matthiasmoser
"""
from configparser import ConfigParser
from sqlite3 import OperationalError

import json
import logging
import hashlib, binascii, os
import traceback

import psycopg2

logger = logging.getLogger("sqlconnecter")
logger.setLevel(logging.WARNING)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

class SqlConn:
    '''
    Connection to database
    Methods for interacting with the database

    :param configdict: database connection information
    '''

    def __init__(self, configdict):
        self.configdict = configdict

    def make_conn(self):
        conn = None
        params = self.configdict
        try:
            conn = psycopg2.connect(**params)
        except:
            logger.info("I am unable to connect to the database")
        return conn


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
                self.execute_command(command)
            except OperationalError as msg:
                print("Command skipped: ", msg)


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

    def set_task_on_side(self,cube_id, filepath):
        """
        takes the json file to write tasks into database

        :param cube_id: integer
        :param filepath: json_file
        :return:
        """
        with open(filepath) as json_file:
            data = json.load(json_file)
            for group in data['groups']:
                for task in data[group]['tasks']:
                    self.set_task(cube_id, data[group][task]['side'], task, group)

    def create_task(self,username,cube_id, task_name, group_name):
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
                logger.warning("task schon vorhanden")
        else:
            try:
                self.execute_command("insert into task values (default,'{}','{}', {}, '{}');".format(task_name, group_name, cube_id, username))
            except:
                print("1",traceback.format_exc())
                logger.warning("task schon vorhanden")



    def create_cube(self,cube_id):
        """
        creates cube on the aws database

        :param cube_id: integer
        :return:
        """
        username = "Paula"
        self.execute_command("insert into cube values ({},'{}');".format(cube_id,username))


    def set_task(self,cube_id, side_id, task_name, group_name,username= "Paula"):
        """
        :param cube_id: integer
        :param side_id: integer
        :param task_name: string
        :param group_name: string
        :return: nothing
        """
        #creates and sets tasks if wanted
        #create_task(cube_id ,task_name, group_name)

        id = self.fetch_data("select Task_Id from task where Task_Name = '{}' and Group_name = '{}' and username = '{}' ".format(task_name, group_name, username))
        task_id = id[0][0]

        try:
            print(cube_id,side_id,task_name,group_name)
            self.execute_command("insert into side values ({},{},{});".format(side_id, cube_id, task_id))
        except:
            print("sides vorhanden update side")
            self.execute_command("update side set Task_Id = {} where side_id = {} and cube_id = {};" \
                            .format(task_id, side_id, cube_id))


    def delete_task(self,username, group_name, task_name):
        """

        :param cube_id: integer
        :param group_name: string
        :param task_name: string
        :return: nothing
        """
        self.execute_command(
            "delete from task where(username = {} and group = '{}' and task = '{}');".format(username, group_name, task_name))

    def check_cube(self,cube_id):
        """"
        checks if cube is aready existent

        """
        print("sfsa")
        check = False
        data = self.fetch_data("select * from cube where cube_id = {}".format(cube_id))
        for cube in data:
            if cube_id in cube:
                check = True
        return check

    def write_cube_information_json(self,cube_id):
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





    def write_cube_state_json(self,cube_id):
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


    def fetch_to_list(self,data):
        liste = list()
        for part in data:
            liste.append(part[0])
        return liste

    def fetch_multiple_to_list(self,data):
        liste = list()
        for part in data:
            liste.append(part)
        return liste

    def get_all_tasks(self,username,cubeid):
        return self.fetch_multiple_to_list(self.fetch_data("select task_id,task_name,group_name from task where username = '{}' and (cube_id = {} or cube_id = null);".format(username,cubeid)))

    def get_all_group_name(self,username):
        return self.fetch_to_list(self.fetch_data("select distinct Group_name from Task where username = '{}';".format(username)))

    def get_all_cube_id(self,username):
        return self.fetch_to_list(self.fetch_data("select cube_ID from cube where username = '{}'".format(username)))

    def set_telegram_user(self,username,telegram_username):
        self.execute_command("update auth_user set telegram_id = {} where username = {}".format(telegram_username,username))

    def update_event(self,task_name, cube_id):
    # Group_ID wird ignoriert
        username = self.fetch_data("select username from cube where Cube_ID = {};".format(cube_id))[0][0]
        task_id = self.fetch_data("select Task_Id from task where username = '{}' and Task_Name = '{}';".format(username,task_name))[0][0]

        self.execute_command("update event set end_time = clock_timestamp() where start_time = (select max(start_time) from event);")
        self.execute_command("insert into event values (default, {}, clock_timestamp(), null );".format(task_id))

