#!/usr/bin/env python3
"""
Created on Thu Feb 13 12:50:37 2020

@author: matthiasmoser
"""
from configparser import ConfigParser
from sqlite3 import OperationalError
import json
import psycopg2
import logging

logger = logging.getLogger("sqlconnecter")
logger.setLevel(logging.WARNING)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


def config(filename='config.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def make_conn():
    conn = None
    params = config()
    try:
        conn = psycopg2.connect(**params)
    except:
        logger.info("I am unable to connect to the database")
    return conn


def fetch_data(cmd):
    """
    fetches data from the aws server

    :param cmd: sql command in string format
    :return: the requested data as list of touple
    """
    if "select" in cmd:
        conn = make_conn()
        result = []
        logger.info("Now executing: %s" % (cmd))
        cursor = conn.cursor()
        cursor.execute(cmd)
        raw = cursor.fetchall()
        for line in raw:
            result.append(line)
        cursor.close()
        conn.close()
        return result
    else:
        logger.warning("tryed to fetch data with \
                       a cmd that return nothing")
        return


def execute_command(cmd):
    """
    executes sql cmd on the aws server

    :param cmd: sql cmd in string format
    :return: nothing
    """
    conn = make_conn()
    cursor = conn.cursor()
    logger.info("Now executing: %s" % (cmd))
    cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()
    return


def execute_Scripts_From_File(filename):
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
            execute_command(command)
        except OperationalError as msg:
            print("Command skipped: ", msg)


def create_task_from_json(json_file):
    """
    takes the json file and creates all task that are in it

    :param json_file: json_file
    :return:
    """
    data = json.load(json_file)
    for group in data['groups']:
        for task in data[group]['tasks']:
            create_task(1, task, group)

def set_task_on_side(cube_id, json_file):
    """
    takes the json file to write tasks into database

    :param cube_id: integer
    :param json_file: json_file
    :return:
    """
    data = json.load(json_file)
    for group in data['groups']:
        for task in data[group]['tasks']:
            set_task(cube_id, data[group][task]['side'], task, group)

def create_task(cube_id, task_name, group_name):
    """
    creates task on the aws database

    :param cube_id: integer
    :param task_name: string
    :param group_name: string
    :return: none
    """
    try:
        execute_command("insert into task values ('{}', '{}', {});".format(task_name, group_name, cube_id))
    except:
        logger.warning("task schon vorhanden")


def create_cube(cube_id):
    """
    creates cube on the aws database

    :param cube_id: integer
    :return:
    """
    execute_command("insert into cube values ({});".format(cube_id))


def set_task(cube_id, side_id, task_name, group_name):
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
        execute_command("insert into side values ({},{},'{}','{}');".format(side_id, cube_id, task_name, group_name))
    except:
        execute_command("update side set task_name = '{}' , group_name = '{}' where side_id = {} and cube_id = {};" \
                        .format(task_name, group_name, side_id, cube_id))


def delete_task(cube_id, group_name, task_name):
    """

    :param cube_id: integer
    :param group_name: string
    :param task_name: string
    :return: nothing
    """
    execute_command(
        "delete from task where(cube_Id = {} and group = '{}' and task = '{}');".format(cube_id, group_name, task_name))


def load_state(cube_id):
    sides = fetch_data("select * from side where Cube_ID = {}".format(cube_id))


def get_all_tasks():
    return fetch_data("select task_name from task;")


def get_all_group_name():
    return fetch_data("select group_name from task_group;")


def get_all_cube_id():
    return fetch_data("select cube_ID from cube")
