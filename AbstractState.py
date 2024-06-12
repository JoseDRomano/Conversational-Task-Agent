 
class AbstractState():
    
    
    def __init__(self,intents,message,name,tuple):
        self._state = name
        self._intents = intents
        self._message = message
        self.input = None
        self.current_Intent = None
        self.tuple = tuple
        
    def get_state(self):
        return self._state
    
    def get_intents(self):
        return self._intents
    
    def get_message(self):
        return self._message
    
    def get_intent(self):
        self.current_Intent = intent(self.input)
        return self.current_Intent
    
    def isStateIntent(self):
        return self.current_Intent in self._intents
    
    def nextState(self):
        return self.tuple[(self._state,self.current_Intent)]
    
    
        