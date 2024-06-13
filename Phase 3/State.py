import sys
sys.path.insert(0, '../Phase 1')
sys.path.insert(0, '../Phase 2')

import search
import PlanLLM

WELCOME = "welcome"
SEARCH = "search"
LIST = "list"
RECIPE = "recipe"
INGREDIENTS = "ingredients"
DESC = "description"
STEPS = "steps"

class State():
    
    def __init__(self,intents,message,name,tuple):
        self._state = name
        self._intents = intents
        self._message = message
        self.input = None
        self.current_Intent = None
        self.tuple = tuple
        self.recipe_list = None
        
    def get_state(self):
        return self._state
    
    def get_intents(self):
        return self._intents
    
    def get_message(self):
        return self._message
    
    def set_intent(self,intent):
        self.current_Intent = intent
        
    def get_intent(self):
        return self.current_Intent
    
    def isStateIntent(self):
        return self.current_Intent in self._intents
    
    def nextState(self):
        return self.tuple[(self._state,self.current_Intent)]
    
    def execute(self, client, index_name, input, recipe):
        if(self._state == LIST):
            return search.search_titleEmbedding(client, index_name, input)
        if(self._state == RECIPE):
            PlanLLM.setup_dialog(recipe)
            print()
            print("Ask something!")
            PlanLLM.dialog()
    
    
        