
class OpenhabParameter:
    
    def __init__(self,params):
        self._params = params

    @property
    def method(self):
            return self._get_value('method')

    @property
    def item(self):
        return self._get_value('item') 

    @property
    def value(self):
        return self._get_value('value')

    @property
    def message(self):
        return self._get_value('message') 
    
    @property
    def type(self):
        return self._get_value('type') 

    @property
    def format(self):
        return self._get_value('format') 

    @property
    def isValid(self):
        return isinstance(self._params, dict) and 'method' in self._params and 'item' in self._params  

    def _get_value(self, key):
        if self.isValid: 
            if key in self._params:
                return self._params[key]
        return None
