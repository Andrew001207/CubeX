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

.. __requirements_overview:

Requirements Overview
---------------------

.. __quality_goals:

Quality Goals
-------------

.. __stakeholders:

Stakeholders
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

.. _section-system-scope-and-context:

System Scope and Context
========================

.. __business_context:

Business Context
----------------

**<Diagram or Table>**

**<optionally: Explanation of external domain interfaces>**

.. __technical_context:

Technical Context
-----------------

**<Diagram or Table>**

**<optionally: Explanation of technical interfaces>**

**<Mapping Input/Output to Channels>**

.. _section-solution-strategy:

Solution Strategy
=================

.. _section-building-block-view:

Building Block View
===================

.. __whitebox_overall_system:

Whitebox Overall System
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

.. _section-quality-scenarios:

Quality Requirements
====================

.. __quality_tree:

Quality Tree
------------

.. __quality_scenarios:

Quality Scenarios
-----------------

.. _section-technical-risks:

Risks and Technical Debts
=========================

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

