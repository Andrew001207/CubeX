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

def connect_to_aws ():
    params = config()
    awsConnecter = AwsConnecter(params['host'],params['rootcapath'],params['certificatepath'],params['privatekeypath'],int(params['port']),params['clientid'],params['topic'])
    awsConnecter.connect()
    return awsConnecter

def decode(json_data):
    print(json_data, "decode")
    test = json_data
    test = test.strip("b")
    test = test.strip('"')
    test = test.strip("[]")
    testarray = test.split(",")
    print(testarray)
    return testarray

def insert_into_database(json_data):
    if json_data is not None:
        print(json_data)
        json_array = decode(json_data)
        execute_command("insert into event Values(3,{},clock_timestamp(),clock_timestamp());".format(json_array[2]))

if __name__ == "__main__":
    aws_con = connect_to_aws()
    aws_con.recieve()
    while True:
        time.sleep(1)
        if aws_con.message is not None:
            print("i am not None")
            insert_into_database(aws_con.message) 
            aws_con.message = None
            