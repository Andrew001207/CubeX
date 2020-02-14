#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:49:17 2020

@author: matthiasmoser
"""
from configparser import ConfigParser
from AwsConnector import AwsConnecter
import json
import time
from SqlConnector import execute_command

def config(filename='database.ini', section='AwsConnector'):
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

def receive ():
    params = config()
    awsConnecter = AwsConnecter(params['host'],params['rootcapath'],params['certificatepath'],params['privatekeypath'],int(params['port']),params['clientid'],params['topic'])
    awsConnecter.connect()
    awsConnecter.

def decode(json_data):
    print(json_data)
    test = json_data
    test = test.strip("[]b'")
    testarray = test.split(",")
    testarray[0]= int(testarray[0])
    testarray[1]= int(testarray[1])
    testarray[3]= int(testarray[3])
    print(testarray)
    return testarray

def insert_into_database(json_data):
    if json_data is not None:
        print(json_data)
        json_array = decode(json_data)
        execute_command("insert into event Values(%d,%e,clock_timestamp(),clock_timestamp())"%(json_array[2]))

if __name__ == "__main__":
    json_data = receive()
    insert_into_database(json_data)