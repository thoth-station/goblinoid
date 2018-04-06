Goblinoid
---------

Convert `Goblin <https://github.com/davebshow/goblin>`_ OGM to JanusGraph schema.

This tool provides an automated way to keep your graph database schema in sync with `Goblin <https://github.com/davebshow/goblin>`_ OGM (Object Graph Mapper). Once you define your schema using Goblin's Vertex and Edge classes you can simply pass sources to Goblinoid that will automatically create a groovy script you can run to create your graph database schema.

You can also instruct Goblinoid to create graph database indexes for you automatically from source code. The only thing you need to do is to annotate your Goblin classes so Goblinoid knows what to do for you.

Installation
============

You can simply install Goblinoid from `PyPI <https://pypi.python.org/pypi/goblinoid>`_:

.. code-block:: console

  $ pip3 install goblinoid


Once your Goblinoid is installed you can access its CLI using:

.. code-block:: console

  $ goblinoid --help


Usage - Schema creation
=======================

TBD.


Usage - Creating indexes
========================

TBD.
