from include import appsettings
import json
import os

class IntentResolver:
        
    def __init__(self, intent):
        self._intent = intent
        self._config = None

    def load(self):
        try:
            name = (appsettings.JSON_TEMPLATE) % self._intent
            if os.path.exists(name):
                file = open(name, 'r')
                self._config = json.loads(file.read())
                file.close()
                return True
        except:
            return False
            
    @property
    def intent(self):
        return self._intent

    @property
    def message(self):
        return self._get_value('message')
    
    @property
    def minScore(self):
        if self.hasMinScore:
            return self._get_value('minScore', 0.0)

    @property
    def hasMinScore(self):
        return self._get_value('minScore', 0) > 0 
    
    @property
    def hasEntities(self):
        return len(self._get_value('entities', {})) > 0

    @property
    def hasConnectors(self):
        return len(self._get_value('connections', {})) > 0 

    @property
    def isValid(self):
        return self._intent and isinstance(self._config, dict) 

    def getEntities(self):
        for entity in self._get_value('entities', {}):
            yield IntentEntity(entity)

    def getConnectors(self):
        for conn in self._get_value('connections', {}):
            yield IntentConnection(conn)

    def _get_value(self, key, default = None):
        if self.isValid: 
            if key in self._config:
                return self._config[key]
        return default

class IntentEntity:
    
    def __init__(self,entity):
        self._entity = entity

    @property
    def minScore(self):
        if self.hasMinScore:
            return self._get_value('minScore', 0.0)

    @property
    def hasMinScore(self):
        return self._get_value('minScore', 0) > 0 

    @property
    def required(self):
        return self._get_value('required', True)

    @property
    def typeName(self):
        return self._get_value('type') 
    
    @property
    def missingText(self):
        return self._get_value('missing') 

    @property
    def isValid(self):
        return isinstance(self._entity, dict) and 'type' in self._entity

    def _get_value(self, key, default = None):
        if self.isValid: 
            if key in self._entity:
                return self._entity[key]
        return default

class IntentConnection:
    
    def __init__(self,connection):
        self._connection = connection

    @property
    def channel(self):
        return self._get_value('channel') 
    
    @property
    def parameter(self):
        return self._get_value('parameter') 

    @property
    def isValid(self):
        return isinstance(self._connection, dict) and 'channel' in self._connection

    def _get_value(self, key, default = None):
        if self.isValid: 
            if key in self._connection:
                return self._connection[key]
        return default
