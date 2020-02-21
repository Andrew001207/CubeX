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
import hashlib, binascii, os


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


def create_task_from_json(cube_id, file_path):
    """
    takes the json file and creates all task that are in it

    :param json_file: json_file
    :return:
    """
    with open(file_path) as json_file:
        data = json.load(json_file)
        for group in data['groups']:
            for task in data[group]['tasks']:
                create_task(cube_id, task, group)

def set_task_on_side(cube_id, filepath):
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
        print(cube_id,side_id,task_name,group_name)
        execute_command("insert into side values ({},{},'{}','{}');".format(side_id, cube_id, task_name, group_name))
    except:
        print("sides vorhanden update side")
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

def check_cube(cube_id):
    """"
    checks if cube is aready existent

    """
    check = False
    data = fetch_data("select * from cube where cube_id = {}".format(cube_id))
    for cube in data:
        if cube_id in cube:
            check = True
    return check
def write_cube_information_json(cube_id):
    #all the tasks,
    groups = fetch_data("select distinct group_name from task where cube_id = {};".format(cube_id))
    tasks = fetch_data("select * from task where cube_id = {};".format(cube_id))
    events = fetch_data("select * from event where cube_id = {};".format(cube_id))
    data = {}
    data['groups'] = []
    for group in groups:
        data['groups'].append(group[0])
        data[group[0]] = []
    for task in tasks:
        data[task[1]].append(task[0])
    data['events'] = []
    for event in events:
        data['events'].append([event[1],event[2],event[4],event[5]])
    return data





def write_cube_state_json(cube_id):
    sides = fetch_data("select * from side where Cube_ID = {}".format(cube_id))
    data = {}
    data['side']= []
    for side in sides:

        data['side'].append(
            {
                'side': side[0],
                'cube_id': side[1],
                'task': side[2],
                'group': side[3]

            }
        )
    return data

def get_all_tasks():
    return fetch_data("select task_name from task;")


def get_all_group_name():
    return fetch_data("select group_name from task_group;")


def get_all_cube_id():
    return fetch_data("select cube_ID from cube")


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def create_user(user_name,user_password):
    hash = hash_password(user_password)
    execute_command("insert into account values ('{}','{}',NULL );".format(user_name,hash))

def update_event(side, cube_id):
    data = fetch_data("select group_name, task_name from side where side_id = {} and cube_id = {}".format(side, cube_id))
    execute_command("update event set end_time = clock_timestamp() where start_time = (select max(start_time) from event);")
    execute_command("insert into event values (default , '{}', '{}', {}, clock_timestamp(), null );".format(data[0][1], data[0][0], cube_id))

print(write_cube_information_json(1))