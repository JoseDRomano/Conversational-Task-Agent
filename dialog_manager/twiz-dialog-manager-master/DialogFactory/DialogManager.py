from DialogFactory.DialogElements import AbstractState
from states import *
from states.WelcomeState import WelcomeState

class DialogManager :

    def __init__(self, start_state = WelcomeState()):
        self.states = AbstractState.__subclasses__()
        self.transitions = {}
        self.current_state = start_state
        #self.history = []

        #print(self.states)
        for state in self.states:
            state_transitions = state.register_transitions()
            self.transitions.update(state_transitions)
        #    if any(t in state_transitions for t in state_transitions) : print("Warning: Transitions conflict")

        #print(self.transitions)
        #print(self.current_state)

    def trigger(self, event) :
        if (self.current_state.__class__, event) in self.transitions:
            self.current_state.event_out(event)
            next_state = self.transitions[(self.current_state.__class__, event)]
            next_state.event_in(event)
            self.current_state = next_state
            #self.history.append(self.current_state)
        else :
            #do something, reprompt?
            print("No transition found for this event")
        return