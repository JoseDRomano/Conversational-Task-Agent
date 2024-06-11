States
==========================================

States have associated events to define accepted transitions to the state.
The abstract code for a state can be seen below:

.. code-block::

    class AbstractState(ABC):

        # define all events
        def __init__(self):
            # { event: function, ... }
            pass

        # operations done when entering the state
        def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]:
            pass

        # operations done when leaving the state
        def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
            pass

        # define transitions from other states to this state with events
        # last_state --- [event,...] ---> self_state
        @staticmethod
        def register_transitions_in() -> dict:
            pass

        # define transitions from other states in a flow to this state with events
        # flow --- [event,...] ---> self_state
        @staticmethod
        def register_subflow_transitions_in() -> dict:
            pass

Create
------------------------------------------

In order to create a state the following steps should be followed:

1. Create a class that inherits from AbstractState and the flow associated with that state

.. code-block::

    class WelcomeState(AbstractState, BackboneFlow):
        ...

2. Override register_transitions_in and register_subflow_transitions_in methods

Use register_transitions_in to define transitions to the state by creating a dictionary with keys as
the states that can transition to the state being defined and values as the events that trigger the transition.

.. code-block::

    @staticmethod
    def register_transitions_in -> dict:
        return {
            ...
            LaunchState: [LaunchIntent],
            ...
        }

If you aim to define a transition that encompasses all of the states related to a certain subflow, make use of
register_subflow_transitions_in, which is exactly the same as the latter but for subflows.

.. code-block::

    @staticmethod
    def register_subflow_transitions_in -> dict:
        return {
            ...
            BackboneFlow: [GreetIntent],
            ...
        }

3. Create event functions for every variation of an action that could be called when an event is received

This event function should return an event if necessary, as well as the name of the response generator that will produce the reply.
An example of an event handling function is the following:

.. code-block::

    def event_greet(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]
        ...
        return None, WelcomeResponder.execute(state_manager)

For information in how to define response generators go to :doc:`response`
The returned event can be used to transition to another state, making it so that the final response is the concatenation of both states responses

.. code-block::

    def event_greet(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]
        ...
        if random.random() > 0.8:
            return MakeSuggestionEvent(), WelcomeResponder.execute(state_manager)
        return None, WelcomeResponder.execute(state_manager)

4. Define what events should call those functions in the state's constructor

.. code-block::

    def __init__(self):
        self.event_functions = {
            LaunchIntent: self.event_present,
            WelcomeIntent: self.event_welcome
        }

Plug in
------------------------------------------

To extend the flow with that state, add it to the flow's __init__.py file

.. code-block::
    
    __all__ = [..., 
           'welcome_state', 
           ...]

Unplug
------------------------------------------

In order to remove a state from the flow, simply comment it out on the __init__.py file of the flow where it's inserted

.. code-block::

    __all__ = [..., 
           #'welcome_state', 
           ...]

