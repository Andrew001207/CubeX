#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:57:35 2020

@author: matthiasmoser
"""
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json

class AwsConnecter:
    '''
        Class which uses the myAWSIoTMQQTTClient to connect with AWS
        this class is specified for the pupurse of the Cube
        
    '''
    def __init__(self, host, rootCAPath, certificatePath, privateKeyPath,\
                 port, clientId, topic):
        self.host = host
        self.rootCAPath = rootCAPath
        self.certificatePath = certificatePath
        self.privateKeyPath = privateKeyPath
        self.port = port
        self.clientId = clientId
        self.topic = topic
        
    def connect(self):
        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = None

        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId)
        self.myAWSIoTMQTTClient.configureEndpoint(self.host, self.port)
        self.myAWSIoTMQTTClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()
        
    def send(self, message):
        messageJson = json.dumps(message)
        self.myAWSIoTMQTTClient.publish(self.topic, messageJson, 1)
        
    def recieve(self):
        self.myAWSIoTMQTTClient.subscribe(self.topic, 1, self.customCallback)
        
    def logger(self):
        self.logger = logging.getLogger("AWSIoTPythonSDK.core")
        self.logger.setLevel(logging.WARNING)
        self.streamHandler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamHandler)
    
    def customCallback(self, client, userdata, message):
        print(message.payload)
        return message.payload


if __name__ == "__main__":
    #this is only implimented as a little test
    aws_connector = AwsConnecter('a19iauu3f7q9ce-ats.iot.us-west-2.amazonaws.com',\
                                 'cert/AmazonRootCA1.pem','cert/5582d73565-certificate.pem.crt',\
                                     'cert/5582d73565-private.pem.key',8883,'Cube','/CubeX_main')
    aws_connector.connect()
    while True:
        aws_connector.recieve()
        time.sleep(1)
        

    