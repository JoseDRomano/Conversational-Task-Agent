from example.events.intent_events.NextIntent import NextIntent


class LastStepEvent(NextIntent):
    id = "LastStepEvent"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return NextIntent.is_valid(state_manager)  # and condition
