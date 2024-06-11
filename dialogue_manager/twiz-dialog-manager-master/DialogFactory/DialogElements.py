from abc import ABC

class AbstractEvent(ABC):
    def __init__(self):
        pass
        
class AbstractState(ABC):
    def __init__(self):
        pass

    def event_in(self, event) :
        pass

    def event_out(self, event) :
        pass

    @staticmethod
    def register_transitions() -> dict:
        pass