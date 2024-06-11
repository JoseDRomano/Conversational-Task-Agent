from DialogFactory.DialogElements import AbstractState

class QuestionVQA(AbstractState):

    def __init__(self):
        self.data = []

    def event_in(self, event) :
        return

    def event_out(self, event) :
        return

    @staticmethod
    def register_transitions() -> dict:
        return {}
