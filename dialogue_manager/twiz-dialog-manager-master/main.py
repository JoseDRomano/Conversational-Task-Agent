from DialogFactory.DialogManager import DialogManager
from events import *

def runDialogManager():
    twiz = DialogManager()

    twiz.trigger(AMAZON_HelpIntent)
    twiz.trigger(AMAZON_StopIntent)

if __name__ == "__main__":
    runDialogManager()
