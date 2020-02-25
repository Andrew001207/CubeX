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

from config_aware import ConfigAware
class CubeX(ConfigAware):

    def __init__(self, cubeId):
        self.cubeId = cubeId
        self.sql_connection = self.conf_db
        self.clientId = 'Manager_' + str(cubeId)
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

    def setTask(self, task_id, side_id, username):
        self.sql_connection.set_task(self.cubeId, side_id, task_id, username= "Paula")
        pass

    def create_Task(self, group_name, task_name, username):
        self.sql_connection.create_task(username, self.cubeId, task_name, group_name)
        pass

    def deleteTask(self, group_name, task_name, username):
        self.sql_connection.delete_task(username, group_name, task_name)
        pass

    def loadState(self):
        json = self.sql_connection.write_cube_state_json(self.cubeId)
        self.connection.send('/CubeX/{}/tasks'.format(self.cubeId), json)
        pass

    def taskMessageAction(self, client, userdata, message):
        cube_response = str(message.payload)
        cube_response = cube_response.strip("b")
        cube_response = cube_response.strip("'")
        cube_response = cube_response.strip("{}")
        cube_response = cube_response.split(":")
        cube_response = cube_response[1].strip('"')
        self.sql_connection.update_event(cube_response, self.cubeId)
        #update_event(a, self.cubeId)
        pass

    def start(self):
        if self.sql_connection.check_cube(self.cubeId) == True:
            self.loadState()
        self.connection.subscribe('/CubeX/{}/status'.format(self.cubeId), self.taskMessageAction)
        while True:
            time.sleep(1)

    def get_cube_id(self):
        return self.cubeId
