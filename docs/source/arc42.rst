.. _section_project_documentation:

Project Documentation
*********************

Documentation on the short-term project at OPNU in Odessa

Project: Smart Cube

.. ___project_participants:

Project Participants
--------------------
+------------------------|--------------+
|Participant             |Student Number|
+========================|==============+
|Kilian Drechsler        |1111111       |
+------------------------|--------------+
|Maximilian Diesenbacher |2050504       |
+------------------------|--------------+
|Florian Wöster          |2222222       |
+------------------------|--------------+
|Matthias Moser          |3333333       |
+------------------------|--------------+

.. __section-introduction-and-goals:

Introduction and Goals
======================
.. ___what_is_the_smart_cube:

What is the Smart Cube?
-----------------------
The project is all about the so called Smart Cube. That is a device with n sides which supports people with their time management. 
To do so you can assign any custom task like cooking, eating, coding, debugging, etc. to each side of the cube and then, when you 
are doing one of these tasks, you simply turn the cube onto the side, you assigned this task to before and after finishing, you turn
the cube to another side and the cube measures the time you spent on that task and later creates you statistics about how much time 
you have spent on which task for example. 

.. ___our_task:

Our Task
--------
Our contribution to the whole Smart Cube project is the creation of an API to communicate with the cube and the database, which also has 
to be created, the creation of a simple Web-GUI to view some statistics of the cube and finally the implementation of a telegram bot to 
configure and work with the cube.  

.. ___how_to_start:

How to start
------------
To see and try the results of the project, the database, the GUI and the bot have to be running in the cloud and the prototype of the cube 
should be connected to a network. If all of this is done, you can connect to the GUI, create a account (with your telegram username) if you 
have not done so yet and connect to the telegram bot where you have to enter "[/]start" to start interacting with the cube.

.. ___requirements_overview:

Requirements Overview
---------------------
As the cube should be a modern and flexible IoT device, the communication will be **cloud based**, in this case using AWS. For lightweight 
and fast interaction with the cube, the **protocol MQTT** is used. And finally considering the expected flexibility and the prototyp state 
of the project, the software components will be implemented in **python**.

.. ___quality_goals:

Quality Goals
-------------
+------------------------|---------------------------------------------------------------------+
|Quality goal            |Motivation and Explanation                                           |
+========================|=====================================================================+
|Flexibility             |At the time of this project, the whole Smart Cube project is still   |
|                        |quite at the beginning. That is why one main quality goal of this    |
|                        |project is to create a flexible and easily expandable software for   |
|                        |future ideas and changes in the whole project .                      |
+------------------------|---------------------------------------------------------------------+
|Functionality and       |The bot and the web GUI should offer a number of basic functions to  |
|Correctness             |interact via a correctly funtioning API with the cube.               |      
+------------------------|---------------------------------------------------------------------+
|Usability               |The bot and the web GUI should be a simple and easy to understand    |
|                        |interface for the user to work with the cube.                        |
+------------------------|---------------------------------------------------------------------+

.. __section-system-scope-and-context:

System Scope and Context
========================

AWS: To connect to the AWS servers with python, the module AWSIoTPythonSDK will be used
Database: As the database will also run on AWS, the there available postgresql will be used
Telegram: For the bot to interact with telegram, the module python-telegram-bot will be used
Web-GUI: The small web-GUI will also be implemented in python with the help of the django framework
table!
.. ___external_interfaces

External Interfaces
-------------------
+------------------------|------------------------------------------------------------------------+
|External system         |Used Interface                                                          |
+========================|========================================================================+
|AWS                     |AWSIoTPythonSDK python package                                          |
+------------------------|------------------------------------------------------------------------+
|Telegram                |python-telegram-bot python package                                      |
+------------------------|------------------------------------------------------------------------+
|Database                |psycopg2 python package to communicate with the database vial postGreSql|
+------------------------|------------------------------------------------------------------------+

.. ___other_dependencies

Other Dependencies
------------------
+------------------------|------------------------------------------------------------------------+
|System                  |Used Component                                                          |
+========================|========================================================================+
|Web GUI                 |Django Webframework for python                                          |
+------------------------|------------------------------------------------------------------------+

.. __section-solution-strategy:

Solution Strategy
=================
.. ___api:

API
---
The API to interact with the cube for now consists of four basic classes. First there is the SqlConnector which interacts directly with the 
database and second the AwsConnector to handle the connection to the AWS and therefore to the cube. Built on those two classes there is the 
class CubeX which represents a cube and handles operations connected directly to the cube like connecting to it or mapping a task onto a 
side of the cube. The other class, called UserX, represents the user and deals with requests only connected to the user like creating tasks. 
These two classes make up the interface to be used by any GUI, Application, etc. to interact with the cube and the database like our bot.

.. ___database:

Database
--------
The database currently consists of five tables. One to hold the users, one for the cubes, one for the tasks, one for the cube side mappings 
and one to store the activities measured by the cube. Within this structure, the cubes and tasks are each bound to a user, a task 
additionally contains a group, which toghter with the user and the name of the task identify it. As a group has to contain at least one task, 
all groups can be found with the tasks. The table for the cube sides identifys a side via a side number and the cube and holds the task that 
was mapped onto the side. Finally the measured activities, called events, contain the task and a start and end time.

.. ___telegram_bot:

Telegram Bot
------------
At first, the idea was to create a bot based on the class ConvHandler of the used telegram API. But as this class in the end came out to be 
too restrictive for a simple and flexible bot, the bot is now made up of two classes. The first one is a custom handler for telegram updates 
to handle multiple users called UserProxy and the actual conversation is handeled by a own state machine implemented in the class 
ConvMachine.

.. ___web_gui:

Web-GUI
-------
As for the architecture pattern Django itself uses the MVC Pattern or in Django’s case a MTC Pattern.
All of our Databases is written down in the models file which resembles the Models in MVC. As well as some extra information.
For our view we have the templates which are written down in html including some java script and Django internal syntax.
The Controller which does almost all the computing work, is located in the views.py file.
It passes all the information to the templates.
The Websites itself has some simple functions, logging in, signing up. As well as editing your Cubes. Along with these Basics functions 
it shows you a few charts which resembles your time spend on the Tasks and Groups.

.. __section-building-block-view:

Building Block View
===================
.. image:: images/Database.pdf
sql conncector

.. image:: images/CubeX.jpg
cubeX + userX

.. image:: images/StateMachine.jpg

.. __section-runtime-view:

Runtime View
============

.. ___bot_conversation:

Bot Conversation
----------------
.. image:: images/RuntimeBot.jpg
To understand the behavior of the bot better, this shows the general procedure of how the user bot interaction works inside the telegram 
bot.

.. ___transmission_to_cube

Transmission to Cube
--------------------
json example
cube sends only task_name, rest callback cubeX
mqtt topics

.. __section-deployment-view:

Deployment View
===============
.. image:: images/Deployment.jpg
Like mentioned in the requirements section, the system should be mainly cloud based, so in the end, the database, the MQTT broker, the 
server for the Web-GUI and the bot should all run in the AWS cloud and the cube and the user communicate via the cloud with eachother. So 
the cube should communicate with the MQTT broker via MQTT and the user can use the Web-GUI or the telegram bot to interact with the cube. 
These two applications then also can communicate via the cube API with the MQTT broker and on this way interact with the cube. 
As for this project itself it was not necessary to let all of this run in the cloud, the Web-GUI and the bot still ran on our local devices 
for easier testing.

.. __section-design-decisions:

Design Decisions
================
As this project is only a small part of the whole Smart Cube project and one of the goals was to create a very flexible software system, 
there were no decicions with too much impact made. The only rather enduring decicions made concern the structure of the database and the 
format of the to the cube transmitted json file itself, because there are already many parts in the software that depend on these 
structures, so changes there could cause a rising number of modifications to be necessary.
db special, modular for flexibility
???
To create a quiet structured way for the user to manage his tasks, the decicions were 
made that on the one hand a group has to contain at least one task, so the user can group his tasks by group and on the other hand a task 
can contain an optional cube_id so the user can also group his tasks by cube.
json
registration
no registration, username telegram = username db
state name conventions
