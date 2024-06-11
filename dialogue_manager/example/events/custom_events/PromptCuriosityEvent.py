from example.events.intent_events.CuriosityIntent import CuriosityIntent


class PromptCuriosityEvent(CuriosityIntent):
    id = "PromptCuriosityEvent"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return CuriosityIntent.is_valid(state_manager)  # and condition
