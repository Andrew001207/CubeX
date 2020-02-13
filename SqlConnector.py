#!/usr/bin/env python3
"""
Created on Thu Feb 13 12:50:37 2020

@author: matthiasmoser
"""

import psycopg2
import logging
db_host = 'cubex-db.cc4xdtflaafw.us-west-2.rds.amazonaws.com'
db_port = 5432
db_name = "cubex"
db_user = "postgres"
db_pass = "7E1TrepkaITJkGfSX7UP"

logger = logging.getLogger("sqlconnecter")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def make_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"\
                                % (db_name, db_user, db_host, db_pass))
    except:
        logger.info("I am unable to connect to the database")
    return conn


def fetch_data(conn, cmd):
    if "selct" in cmd:
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


def excecute_command(conn, cmd):
    cursor = conn.cursor()
    logger.info("Now executing: %s" % (cmd))
    cursor.execute(cmd)
    cursor.close()
    conn.close()
    return

#bsp how to use
#excecute_command(make_conn(),"drop table event")