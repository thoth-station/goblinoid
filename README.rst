Goblinoid
---------

Convert `Goblin <https://github.com/davebshow/goblin>`_ OGM to JanusGraph schema.

This tool provides an automated way to keep your graph database schema in sync with `Goblin <https://github.com/davebshow/goblin>`_ OGM (Object Graph Mapper). Once you define your schema using Goblin's Vertex and Edge classes you can simply pass sources to Goblinoid that will automatically create a groovy script you can run to create your graph database schema.

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

Goblinoid allows you to automatically create schema based on models defined in your source code. To automatically generate schema definition, you need to point Goblinoid to the correct module of your application that holds all defined models for your application:


.. code-block:: console

  $ goblinoid-cli --module-import 'myapp.graph.models' --models-iterable 'ALL_MODELS' --schema-file schema.groovy


.. tip::

  By using one iterable (e.g. tuple), you can directly reuse this iterable for the `Goblin's register <http://goblin.readthedocs.io/en/latest/ogm.html#saving-elements-to-the-database-using-session>`_ method to keep your models always in sync in your application:

  .. code-block:: python

        app = await Goblin.open(
            loop,
            hosts=['localhost'],
            port=port,
        ))
        app.register(*tuple(ALL_MODELS))


It's important to state that your package/module is importable for the CLI (you might want to adjust ``PYTHONPATH`` to accomplish that in some cases). Goblinoid automatically creates a Groovy script that you can run to create schema.

It is **recommended** to also provide the ``--schema-vertex-identifier`` option. In that case Goblinoid automatically creates a vertex with label ``goblinoid_schema_meta`` that holds provided ``identifier`` and ``datetime`` when the schema creation was performed. This allows you to keep graph metadata for later debugging or ensuring your services that communicate with the graph instance use required schema version.

By default, Goblinoid disables JanusGraph's schema maker. It is **recommended** having the schema maker disabled so all vertexes and edges that are added to the graph database respect the provided schema and there are not created additional schema entries. You can avoid this behaviour by specifying the ``--keep-schema-maker`` flag. See the `official documentation <http://docs.janusgraph.org/0.2.0/schema.html#_automatic_schema_maker>`_ for more info.

