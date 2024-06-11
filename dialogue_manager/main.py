# these imports are necessary even if not directly used
from example.states import *
from example.events import *

from example.dialog_factory.dialog_manager import DialogManager

# create the dialog manager
dialog_manager = DialogManager()

# define the state manager with the needed variables
state_manager = {"intent": "",
                 "recipe": 0,
                 "step": 1}


def run_dialog_manager():
    while True:
        # receive intent from user utterance
        state_manager["intent"] = input('Intent: ')

        # turn intent into event and trigger a transition in the state machine
        event = dialog_manager.event_type(state_manager)
        response = dialog_manager.trigger(event(), state_manager)

        # input the response
        print("BOT:", response['response'])

        # generate page from HTML in response['screen'] if wanted


if __name__ == "__main__":
    run_dialog_manager()
