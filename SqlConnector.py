#!/usr/bin/env python3
"""
Created on Thu Feb 13 12:50:37 2020

@author: matthiasmoser
"""
from configparser import ConfigParser
import psycopg2
import logging

logger = logging.getLogger("sqlconnecter")
<<<<<<< HEAD
logger.setLevel(logging.INFO)
=======
logger.setLevel(logging.WARNING)
>>>>>>> origin/Momo
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def config(filename='database.ini', section='postgresql'):
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
