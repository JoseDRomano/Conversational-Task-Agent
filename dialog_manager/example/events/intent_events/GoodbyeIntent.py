from example.dialog_factory.dialog_elements import AbstractEvent


class GoodbyeIntent(AbstractEvent):
    id = "GoodbyeIntent"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == GoodbyeIntent.id
