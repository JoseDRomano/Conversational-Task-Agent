from DialogFactory.DialogElements import AbstractState
from events import *
from states.ByeState import ByeState
from states.FallBackState import FallBackState

class ListState(AbstractState):

    def __init__(self):
        self.data = []

    def event_in(self, event) :
        print("The options are: one, two and three.")
        return

    def event_out(self, event) :
        print("Great option!")
        return

    @staticmethod
    def register_transitions() -> dict:
        return {
            (ListState, AMAZON_FallbackIntent) : FallBackState(),
            (ListState, OutOfScopeIntent) : FallBackState(),
            (ListState, AMAZON_StopIntent) : ByeState(),
            (ListState, TerminateCurrentTaskIntent) : ByeState(),
        }
