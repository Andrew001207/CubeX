#!/usr/bin/env python3
"""
Created on Thu Feb 13 12:50:37 2020

@author: matthiasmoser
"""
from configparser import ConfigParser
import psycopg2
import logging

logger = logging.getLogger("sqlconnecter")
logger.setLevel(logging.WARNING)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


def config(filename='database.ini', section= 'postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}    
    params = parser.items(section)
    for param in params:
         db[param[0]] = param[1]
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
    conn = make_conn()
    cursor = conn.cursor()
    logger.info("Now executing: %s" % (cmd))
    cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()
    return

def create_task(task_name,task_group):
    try:
        group_id = fetch_data("select group_ID from Task_group where group_name = '{}'".format(task_group))[0][0]
        execute_command("insert into task values ('{}', {});".format(task_name, group_id))
    except:
        execute_command("insert into task_group values (default,'{}');".format(task_group))
        try:
            execute_command("insert into task values ('{}', {});".format(task_name, group_id))
        except:
            logger.warning("task schon vorhanden")
def create_cube():
    execute_command("insert into cube values (default);")

def assign_task_side(cube_ID, side, task):
    execute_command("insert into side values ('{}','{}','{}');".format(cube_ID,side,task))

def get_all_tasks():
    return fetch_data("select task_name from task;")

def get_all_group_name():
    return fetch_data("select group_name from task_group;")

def get_all_cube_id():
    return fetch_data("select cube_ID from cube")



print(get_all_group_name())






