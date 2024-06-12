Events
==========================================

An event is responsible for triggering a state transition.
It's necessary that, for each intent the intent detector can return, an event is created.
If conditional transitions are needed, a custom event associated with a supported intent can be created as to check an additional condition.

Create
------------------------------------------

Intent event
^^^^^^^^^^^^

The event must inherit from the AbstractEvent class and its id should be the same as the intent name returned by the intent detector.
Its is_valid() method verifies if the event should be triggered, which, in the case of intent events, simply checks if the active intent
is the same as the event id.

.. code-block::

    class GreetingIntent(AbstractEvent):
        id = "GreetingIntent"
        description = ""

        def __init__(self):
            pass

        @staticmethod
        def is_valid(state_manager: {}):
            return state_manager["intent"] == GreetingIntent.id


Custom event
^^^^^^^^^^^^

The event must inherit from the intent event class that is related to it and use its id.
Its is_valid() method verifies if the event should be triggered, which, in the case of custom events, checks if the detected intent
is the same as the event id (by checking if its parent intent is valid) and verifies the additional conditions.

.. code-block::

    class IdentifyRecipeEvent(IdentifyIntent):
        id = IdentifyIntent.id
        description = ""

        def __init__(self):
            pass

        @staticmethod
        def is_valid(state_manager: {}):
            return IdentifyProcessIntent.is_valid(state_manager) and state_manager["type"] == "recipe"

Plug in
------------------------------------------

To make this a valid event in the state machine, it's necessary to add it to the list of events in their events package:
intent_events/__init__.py in the case of intent events or custom_events/__init__.py in the case of custom events.

.. code-block::

    __all__ = [ 
        ...
        'GreetingIntent',
        ...
    ]

Unplug
------------------------------------------

The remove an event from the state machine it's only necessary to comment it out in the list of events in their events package:
intent_events/__init__.py in the case of intent events or custom_events/__init__.py in the case of custom events.

.. code-block::

    __all__ = [ 
        ...
        #'IdentifyRecipeEvent',
        ...
    ]
