Subflows
==========================================

Subflows help in the modularization of the dialog manager. 
They are a way to separate the dialog into different parts that can be plugged in and out of the dialog backbone and define a set of states
that are associated with each other.

Create
------------------------------------------

In order to create a new subflow the following steps must be followed:

1. Add an empty class for a new subflow in the flows.py file present in the dialog_factory folder

.. code-block::

    class HelpFlow:
        def __init__(self):
            return

2. Create a new subflow folder inside states and complement it with a response_generators folder. It's in there that the
    states and response generators associated with the subflow must be added.

.. code-block::

   ├── states
   │   ├── __init__.py
   │   ├── ...
   │   ├── subflow_help
   │   │   ├── __init__.py
   │   │   ├── ...
   │   |   ├── response_generators
   │   |   │   ├── __init__.py
   │   |   │   ├── ...
   │   ├── ...


Plug in
------------------------------------------

In order to plug the subflow in the backbone flow the file states/__init__.py must start importing the created subflow folder.

.. code-block::

    from ..states.subflow_help import *


Unplug
------------------------------------------

In order to plug the subflow out of the backbone flow the file states/__init__.py must stop importing the subflow folder.

.. code-block::

    #from ..states.subflow_help import *

