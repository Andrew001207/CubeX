#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 11:34:30 2020

@author: Andrew001207
# Write edits here:
"""
from sql.aws_Connector import AwsConnecter
from configparser import ConfigParser
import time
import sql.sql_Connector
class CubeX:

    def __init__(self, cubeId,connection):
        self.cubeId = cubeId
        self.sqlconnection = connection
        self.clientId = 'Manager_' + str(cubeId)
        conf = self.loadAWSConfig()
        self.connection = AwsConnecter(
                                        conf['host'],
                                        conf['rootcapath'],
                                        conf['certificatepath'],
                                        conf['privatekeypath'],
                                        int(conf['port']),
                                        self.clientId)
        try:
            self.connection.connect()
            print(self.clientId + ' Successfully connected')
        except Exception:
            print("Fehler")

        # TODO Connect database instance

    def loadAWSConfig(self, path='cert/config.ini', section='AwsConnector'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(path)
        # get section, default to postgresql
        if parser.has_section(section):
            conf = dict(parser.items(section))
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, path))
        return conf

    # TODO Implement following methods

    def setTask(self, group_name, task_name, side_id, username):
        self.sqlconnection.set_task(self.cubeId, side_id, task_name, group_name,username= "Paula")
        pass

    def create_Task(self, group_name, task_name, username):
        self.sqlconnection.create_task(username,self.cubeId, task_name,group_name)
        pass

    def deleteTask(self, group_name, task_name, username):
        self.sqlconnection.delete_task(username, group_name, task_name)
        pass

    def loadState(self):
        json = self.sqlconnection.write_cube_state_json(self.cubeId)
        self.connection.send('/CubeX/{}/tasks'.format(self.cubeId), json)
        pass

    def taskMessageAction(self, client, userdata, message):
        a = str(message.payload)
        a = a.strip("b")
        a = a.strip("'")
        a = a.strip("{}")
        a = a.split(":")
        a = a[1].strip('"')
        self.sqlconnection.update_event(a,self.cubeId)
        #update_event(a,self.cubeId)
        pass

    def start(self):
        if self.sqlconnection.check_cube(a.cubeId) == True:
            a.loadState()
        a.connection.subscribe('/CubeX/{}/status'.format(a.cubeId), a.taskMessageAction)
        while True:
            time.sleep(1)



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

if  __name__ == "__main__":
    print("Test run")
    b = sql.sql_Connector.SqlConn(config())
    a = CubeX(1,b )
    a.start()

    print(b.get_all_tasks("Paula",1))