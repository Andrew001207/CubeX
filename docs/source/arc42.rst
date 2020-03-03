**About arc42**

arc42, the Template for documentation of software and system
architecture.

By Dr. Gernot Starke, Dr. Peter Hruschka and contributors.

Template Revision: 7.0 EN (based on asciidoc), January 2017

© We acknowledge that this document uses material from the arc 42
architecture template, http://www.arc42.de. Created by Dr. Peter
Hruschka & Dr. Gernot Starke.

.. _section-introduction-and-goals:

Introduction and Goals
======================
The project is all about the so called Smart Cube. That is a device with n sides which supports people with their time management. 
To do so you can assign any custom task like cooking, eating, coding, debugging, etc. to each side of the cube and then, when you 
are doing one of these tasks, you simply turn the cube onto the side, you assigned this task to before and after finishing, you turn
the cube to another side and the cube measures the time you spent on that task and later creates you statistics about how much time 
you have spent on which task for example. The contribution of this specific project to the whole Smart Cube project should be the creation 
of an API to communicate with the cube and the database, which also has to be created, the creation of a simple Web-GUI to view some 
statistics of the cube and finally the implementation of a telegram bot to configure and work with the cube.  

.. __how_to_start:

How to start
------------
To see and try the results of the project, the database, the GUI and the bot code have to be running and the prototype of the cube should 
be connected to a network. If all of this is done, you can connect to the GUI, create a account if you have not done so yet and connect to 
the telegram bot where you have to enter "start" to start interacting with the cube.

.. __requirements_overview:

Requirements Overview
---------------------
As the cube should be a modern and flexible IoT device, the communication will be cloud based, in this case using AWS. For lightweight and 
fast interaction with the cube, the protocol MQTT is used. Considering the expected flexibility and the prototyp state of the project, the 
software components may be implemented in python.

.. __quality_goals:

Quality Goals
-------------
At the time of this project, the whole Smart Cube project is still quite at the beginning. That is why the main quality goal of this project 
is flexibility for future ideas and changes in the whole project. Apart from that the main goal is to create a simple, easily expandable and 
correctly working software package for interaction with cube and database.

.. __stakeholders:

(Stakeholders)
------------

+-------------+---------------------------+---------------------------+
| Role/Name   | Contact                   | Expectations              |
+=============+===========================+===========================+
| *<Role-1>*  | *<Contact-1>*             | *<Expectation-1>*         |
+-------------+---------------------------+---------------------------+
| *<Role-2>*  | *<Contact-2>*             | *<Expectation-2>*         |
+-------------+---------------------------+---------------------------+

.. _section-architecture-constraints:

(Architecture Constraints)
========================
???

.. _section-system-scope-and-context:

System Scope and Context
========================
AWS: To connect to the AWS servers with python, the module AWSIoTPythonSDK will be used
Database: As the database will also run on AWS, the there available postgresql will be used
Telegram: For the bot to interact with telegram, the module python-telegram-bot will be used
Web-GUI: The small web-GUI will also be implemented in python with the help of the django framework

.. _section-solution-strategy:

Solution Strategy
=================
API:
The API to interact with the cube for now consists of four basic classes. There is one to interact directly with the database and one 
to handle the connection to the AWS. Built on those two classes there is one class which represents the cube and handles operations 
connected directly to the cube like mapping a task onto a side of the cube. The other class represents the user and deals with requests 
only connected to the user like creating tasks. These two classes are the interface to be used for any GUI, Application, etc. to interact 
with the cube and the database.
DB:
The database currently consists of five tables. One to hold the users, one for the cubes, one for the tasks, one for the cube side mappings 
and one to store the activities measured by the cube.
Bot:
At first, the idea was to create the bot based on the class ConvHandler of the used telegram API. But as this in the end was to restrictive, 
the bot is now made up of two classes. The first one is a custom handler for telegram updates to deal with multiple users and the actual 
conversation is handeled by a own state machine.
Web_GUI:
django, ...???

.. _section-building-block-view:

Building Block View
===================
DB diagramm:
group with task
optional cube_id in task
Class diagramm
state machine

Runtime View
============

.. ___runtime_scenario_1:

<Runtime Scenario 1>
--------------------
Only one scenario

-  *<insert runtime diagram or textual description of the scenario>*

-  *<insert description of the notable aspects of the interactions
   between the building block instances depicted in this diagram.>*

.. _section-deployment-view:

Deployment View
===============
diagram
db on aws, bot maybe aws, mqtt broker aws

.. _section-concepts:

(Cross-cutting Concepts)
======================
???

.. ___emphasis_concept_1_emphasis:

*<Concept 1>*
-------------

*<explanation>*

.. ___emphasis_concept_n_emphasis:

*<Concept n>*
-------------

*<explanation>*

.. _section-design-decisions:

Design Decisions
================
As this project is only a small part of the whole Smart Cube project, there were no decicions with too much impact made. The only slightly 
important decicions concern the structure of the database and the format of the to the cube transmitted json file, because there are 
already many parts in the software that depend on these structures, so changes there could make some bigger modifications necessary.

.. _section-quality-scenarios:

(Quality Requirements)
====================
???

.. __quality_tree:

Quality Tree
------------

.. __quality_scenarios:

(Quality Scenarios)
-----------------

.. _section-technical-risks:

(Risks and Technical Debts)
=========================

.. _section-glossary:

(Glossary)
========

+-----------------------------------+-----------------------------------+
| Term                              | Definition                        |
+===================================+===================================+
| <Term-1>                          | <definition-1>                    |
+-----------------------------------+-----------------------------------+
| <Term-2>                          | <definition-2>                    |
+-----------------------------------+-----------------------------------+