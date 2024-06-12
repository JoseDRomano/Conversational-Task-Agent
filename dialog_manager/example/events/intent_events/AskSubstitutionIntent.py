from example.dialog_factory.dialog_elements import AbstractEvent


class AskSubstitutionIntent(AbstractEvent):
    id = "AskSubstitutionIntent"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == AskSubstitutionIntent.id
