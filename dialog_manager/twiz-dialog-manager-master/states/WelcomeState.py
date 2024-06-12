from DialogFactory.DialogElements import AbstractState
from events import *
from states.FallBackState import FallBackState
from states.ListState import ListState
from states.ByeState import ByeState

class WelcomeState(AbstractState) :

    def __init__(self):
        self.data = []

    def event_in(self, event) :
        print("Welcome to twiz. This is a toy example of an open State Machine.")
        return

    def event_out(self, event) :
        print("There's nothing to clean up.")
        return

    @staticmethod
    def register_transitions() -> dict:
        return {
            (WelcomeState, AMAZON_HelpIntent) : ListState(),
            (WelcomeState, AMAZON_FallbackIntent) : FallBackState(),
            (WelcomeState, OutOfScopeIntent) : FallBackState(),
            (WelcomeState, AMAZON_StopIntent) : ByeState(),
            (WelcomeState, TerminateCurrentTaskIntent) : ByeState(),
        }
