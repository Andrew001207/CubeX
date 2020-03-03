#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import traceback
import time

from sql.aws_connector import AwsConnector
from sql.sql_connector import SqlConnector
from config_aware import ConfigAware


LOGGER = logging.getLogger("sqlconnector")
LOGGER.setLevel(logging.WARNING)
STREAM_HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
STREAM_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(STREAM_HANDLER)

class CubeX(ConfigAware):
    "Representation of a Cube"
    def __init__(self, cube_id):
        super().__init__()
        self.cube_id = cube_id
        self.sql_connection = SqlConnector()
        self.client_id = 'Manager_' + str(cube_id)
        self.connection = AwsConnector(
            self.conf_aws['host'],
            self.conf_aws['rootcapath'],
            self.conf_aws['certificatepath'],
            self.conf_aws['privatekeypath'],
            int(self.conf_aws['port']),
            self.client_id)
        try:
            self.connection.connect()
            LOGGER.info('%s Successfully connected', self.client_id)
        except Exception:
            raise Exception('Could not establish a connection to Amazon cloud Services')
        self.start()
    def set_task(self, task_id, side_id):
        '''maps a task on a cube side'''

        self.sql_connection.set_task(self.cube_id, side_id, task_id)
        self.load_state()

    def load_state(self):
        '''sends the tasks to aws'''
        json = self.sql_connection.write_cube_state_json(self.cube_id)
        self.connection.send('/CubeX/{}/tasks'.format(self.cube_id), json)

    def task_message_action(self, client, userdata, message):
        "Callback function after a side change of the cube"
        cube_response = str(message.payload)
        cube_response = cube_response.strip("b")
        cube_response = cube_response.strip("'")
        cube_response = cube_response.strip("{}")
        cube_response = cube_response.split(":")
        cube_response = cube_response[1].strip('"')
        self.sql_connection.update_event(cube_response, self.cube_id)
        #update_event(a, self.cube_id)

    def start(self):
        "starts the connection"
        if self.sql_connection.check_cube(self.cube_id):
            self.load_state()
        self.connection.subscribe('/CubeX/{}/status'.format(self.cube_id), self.task_message_action)

    def get_cube_id(self):
        "getting the cube id"
        return self.cube_id

    def get_side_tasks(self):
        return self.sql_connection.get_side_info(self.cube_id)
        
