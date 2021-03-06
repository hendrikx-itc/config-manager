Config Manager
==============

A set of tools for managing configuration using a single source of truth in
the form of versioned yaml based data. Next to built-in output formats, you can
use custom Jinja based templates for generating text based output formats.

The Config Manager is normally used with a configuration stored in a git
repository, with a config file named `.config_manager` in the root of the git
repository.

Installation
============

Install from the sources in this repository::

    $ pip install -U .

Configuration
=============

Configuration is done using a config file named `.config_manager` in the root
of the git repository. So to start a new project, you could use the following
commands::

    $ git init my-configuration

    $ config init my-configuration


Example Custom Jinja Template
=============================

Here we generate output from the provided test data and an example template::

    $ config jinja example/template_1.jinja example/configuration_1.yml
    # Nodes

    host: web

    host: app_1

    host: app_2

    host: app_3

    host: app_db_conn_pool

    host: app_db_1

    host: app_db_2

    host: app_db_3

This simple template has a static header and a list of all the hosts with their
names printed.
