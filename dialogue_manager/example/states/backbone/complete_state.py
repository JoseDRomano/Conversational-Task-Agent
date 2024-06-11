from typing import Optional, Tuple
from example.dialog_factory.dialog_elements import AbstractState, AbstractEvent
from example.dialog_factory.flows import BackboneFlow
from example.events.intent_events.GoodbyeIntent import GoodbyeIntent
from example.events.custom_events.LastStepEvent import LastStepEvent


class CompleteState(AbstractState, BackboneFlow):

    def __init__(self):
        self.event_functions = {
            GoodbyeIntent: self.event_dummy,
            LastStepEvent: self.event_dummy
        }

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]:
        return self.event_functions[type(event)](event, history, state_manager)

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
        return

    @staticmethod
    def register_transitions_in() -> dict:
        from example.states.backbone.step_state import StepState
        return {
            StepState: [LastStepEvent, GoodbyeIntent]
        }

    @staticmethod
    def register_subflow_transitions_in() -> dict:
        return {}

    def event_dummy(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]:
        return None, {'response': ""}
