#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 11:34:30 2020

@author: Andrew001207
# Write edits here:
"""
from sql.aws_Connector import AwsConnecter
from configparser import ConfigParser
from sql.sql_Connector import set_task, delete_task, write_cube_state_json, create_task, create_cube, check_cube, update_event
import time

class CubeX:

    def __init__(self, cubeId):
        self.cubeId = cubeId
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
        except Exception as e:
            print(e.message)

        # TODO Connect database instance

    def loadAWSConfig(self, path='config.ini', section='AwsConnector'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(path)
        # get section, default to postgresql
        conf = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                conf[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, path))
        return conf

    # TODO Implement following methods

    def setTask(self, group, name, side):
        set_task(self.cubeId, side, name, group)
        pass

    def create_Task(self, group, name):
        create_task(self.cubeId, group, name)
        pass

    def deleteTask(self, group, name):
        delete_task(self.cubeId, group, name)
        pass

    def loadState(self):
        json = write_cube_state_json(self.cubeId)
        self.connection.send('/CubeX/{}/tasks'.format(self.cubeId), json)
        pass

    def taskMessageAction(self, client, userdata, message):
        a = str(message.payload)
        a = a.strip('b')
        a = a.strip("'")
        update_event(a,self.cubeId)
        pass

    def start(self):
        if check_cube(a.cubeId) == True:
            a.loadState()
        a.connection.subscribe('/CubeX/{}/status'.format(a.cubeId), a.taskMessageAction)
        while True:
            time.sleep(1)
