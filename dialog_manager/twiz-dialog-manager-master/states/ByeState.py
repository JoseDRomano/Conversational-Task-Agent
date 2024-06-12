from DialogFactory.DialogElements import AbstractState

class ByeState(AbstractState):

    def __init__(self):
        self.data = []

    def event_in(self, event) :
        print("Good bye! Hope to see you soon.")
        return

    def event_out(self, event) :
        print("There's nothing to clean up.")
        return

    @staticmethod
    def register_transitions() -> dict:
        return {}
