from typing import Optional, Tuple
from example.dialog_factory.dialog_elements import AbstractState, AbstractEvent
from example.dialog_factory.flows import BackboneFlow
from example.events.intent_events.SpecifyStepIntent import SpecifyStepIntent
from example.events.intent_events.PreviousIntent import PreviousIntent
from example.events.intent_events.AffirmIntent import AffirmIntent
from example.events.intent_events.NextIntent import NextIntent


class StepState(AbstractState, BackboneFlow):

    def __init__(self):
        self.event_functions = {
            SpecifyStepIntent: self.event_dummy,
            PreviousIntent: self.event_dummy,
            AffirmIntent: self.event_dummy,
            NextIntent: self.event_dummy
        }

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]:
        return self.event_functions[type(event)](event, history, state_manager)

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
        return

    @staticmethod
    def register_transitions_in() -> dict:
        from example.states.backbone.choice_state import ChoiceState
        return {
            ChoiceState: [AffirmIntent],
            StepState: [PreviousIntent, NextIntent, SpecifyStepIntent]
        }

    @staticmethod
    def register_subflow_transitions_in() -> dict:
        return {}

    def event_dummy(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]:
        return None, {'response': ""}
