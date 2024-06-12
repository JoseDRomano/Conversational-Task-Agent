from typing import Optional, Tuple
from example.dialog_factory.dialog_elements import AbstractState, AbstractEvent
from example.dialog_factory.flows import CuriosityFlow, BackboneFlow
from example.events.intent_events.CuriosityIntent import CuriosityIntent
from example.events.intent_events.AffirmIntent import AffirmIntent


class CuriosityState(AbstractState, CuriosityFlow):

    def __init__(self):
        self.event_functions = {
            CuriosityIntent: self.event_dummy,
            AffirmIntent: self.event_dummy
        }

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]:
        return self.event_functions[type(event)](event, history, state_manager)

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
        return

    @staticmethod
    def register_transitions_in() -> dict:
        from example.states.subflow_curiosity.prompt_curiosity_state import PromptCuriosityState
        return {
            PromptCuriosityState: [AffirmIntent]
        }

    @staticmethod
    def register_subflow_transitions_in() -> dict:
        return {
            BackboneFlow: [CuriosityIntent]
        }

    def event_dummy(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], dict]:
        return None, {'response': ""}
