from example.dialog_factory.dialog_elements import AbstractEvent


class StopIntent(AbstractEvent):
    id = "StopIntent"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == StopIntent.id
