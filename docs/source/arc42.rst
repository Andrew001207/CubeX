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
mqtt
python, os independent, prototype
cloud based

.. __quality_goals:

Quality Goals
-------------
easy to add functions
os independent
flexible
other guis


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

Architecture Constraints
========================
???

.. _section-system-scope-and-context:

System Scope and Context
========================

.. __business_context:

(Business Context)
----------------

**<Diagram or Table>**

**<optionally: Explanation of external domain interfaces>**

.. __technical_context:

Technical Context
-----------------
AWS, telegram API, sql

**<Diagram or Table>**

**<optionally: Explanation of technical interfaces>**

**<Mapping Input/Output to Channels>**

.. _section-solution-strategy:

Solution Strategy
=================
API:
sql_connector
cubeX
userX
DB:
user, cube, task, side, event
Bot:
user-management
state machine
Web_GUI:
django, ...

.. _section-building-block-view:

Building Block View
===================
DB diagramm
Class diagramm
state machine

.. __whitebox_overall_system:

(Whitebox Overall System)
-----------------------

**<Overview Diagram>**

Motivation
   *<text explanation>*

Contained Building Blocks
   *<Description of contained building block (black boxes)>*

Important Interfaces
   *<Description of important interfaces>*

.. ___name_black_box_1:

<Name black box 1>
~~~~~~~~~~~~~~~~~~

*<Purpose/Responsibility>*

*<Interface(s)>*

*<(Optional) Quality/Performance Characteristics>*

*<(Optional) Directory/File Location>*

*<(Optional) Fulfilled Requirements>*

*<(optional) Open Issues/Problems/Risks>*

.. ___name_black_box_2:

<Name black box 2>
~~~~~~~~~~~~~~~~~~

*<black box template>*

.. ___name_black_box_n:

<Name black box n>
~~~~~~~~~~~~~~~~~~

*<black box template>*

.. ___name_interface_1:

<Name interface 1>
~~~~~~~~~~~~~~~~~~

…

.. ___name_interface_m:

<Name interface m>
~~~~~~~~~~~~~~~~~~

.. __level_2:

Level 2
-------

.. __white_box_emphasis_building_block_1_emphasis:

White Box *<building block 1>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. __white_box_emphasis_building_block_2_emphasis:

White Box *<building block 2>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

…

.. __white_box_emphasis_building_block_m_emphasis:

White Box *<building block m>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. __level_3:

Level 3
-------

.. __white_box_building_block_x_1:

White Box <_building block x.1_>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. __white_box_building_block_x_2:

White Box <_building block x.2_>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. __white_box_building_block_y_1:

White Box <_building block y.1_>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. _section-runtime-view:

Runtime View
============

.. ___runtime_scenario_1:

<Runtime Scenario 1>
--------------------
Only one scenario

-  *<insert runtime diagram or textual description of the scenario>*

-  *<insert description of the notable aspects of the interactions
   between the building block instances depicted in this diagram.>*

.. ___runtime_scenario_2:

<Runtime Scenario 2>
--------------------

.. __:

…
-

.. ___runtime_scenario_n:

<Runtime Scenario n>
--------------------

.. _section-deployment-view:

Deployment View
===============
no levels
db on aws, bot maybe aws, mqtt broker aws

.. __infrastructure_level_1:

Infrastructure Level 1
----------------------

**<Overview Diagram>**

Motivation
   *<explanation in text form>*

Quality and/or Performance Features
   *<explanation in text form>*

Mapping of Building Blocks to Infrastructure
   *<description of the mapping>*

.. __infrastructure_level_2:

Infrastructure Level 2
----------------------

.. ___emphasis_infrastructure_element_1_emphasis:

*<Infrastructure Element 1>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<diagram + explanation>*

.. ___emphasis_infrastructure_element_2_emphasis:

*<Infrastructure Element 2>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<diagram + explanation>*

…

.. ___emphasis_infrastructure_element_n_emphasis:

*<Infrastructure Element n>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<diagram + explanation>*

.. _section-concepts:

Cross-cutting Concepts
======================
???

.. ___emphasis_concept_1_emphasis:

*<Concept 1>*
-------------

*<explanation>*

.. ___emphasis_concept_2_emphasis:

*<Concept 2>*
-------------

*<explanation>*

…

.. ___emphasis_concept_n_emphasis:

*<Concept n>*
-------------

*<explanation>*

.. _section-design-decisions:

Design Decisions
================
json???

.. _section-quality-scenarios:

Quality Requirements
====================
???

.. __quality_tree:

Quality Tree
------------

.. __quality_scenarios:

Quality Scenarios
-----------------

.. _section-technical-risks:

Risks and Technical Debts
=========================
weglassen???

.. _section-glossary:

Glossary
========

+-----------------------------------+-----------------------------------+
| Term                              | Definition                        |
+===================================+===================================+
| <Term-1>                          | <definition-1>                    |
+-----------------------------------+-----------------------------------+
| <Term-2>                          | <definition-2>                    |
+-----------------------------------+-----------------------------------+

.. |arc42| image:: images/arc42-logo.png