from example.dialog_factory.dialog_elements import AbstractEvent


class FallbackIntent(AbstractEvent):
    id = "FallbackIntent"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == FallbackIntent.id
