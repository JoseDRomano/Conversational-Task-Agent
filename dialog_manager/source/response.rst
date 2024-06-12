Response Generators
==========================================

Response generators build the response that the agent should reply with.
In less complex agents, where there is no need for much logic, response generators may not be necessary, and the
response can be constructed directly within the state.

Create
------------------------------------------

To create a response generator, a class conforming to the structure outlined below should be added to the response_generators
folder of the flow that holds the state(s) that will invoke it.

.. code-block::

    class WelcomeResponder:

        @staticmethod
        def execute(state_manager: {}) -> dict:
            name = state_manager['name']

            return {'response': f'Welcome {name}, nice to meet you!', 'screen' = '<h1>Welcome</h1>'}

The 'response' field is intended for the agent's text response, whereas the 'screen' field, which is optional,
is used to define the HTML that the agent needs to generate a page if one wants to do so.