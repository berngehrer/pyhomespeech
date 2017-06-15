from include import appsettings
import requests

class OpenhabClient():

    def __init__(self):
        self._header = { 
            "Content-type": "text/plain"
        }

    def post_command(self, key, value):
        url = appsettings.ITEM_PATTERN % (appsettings.MQTT_HOST, key)
        req = requests.post(url, data=value, headers=self._header)
        self.__success(req)

    def put_status(self, key, value):
        url = appsettings.ITEM_STATE_PATTERN % (appsettings.MQTT_HOST, key)
        req = requests.put(url, data=value, headers=self._header)
        self.__success(req)

    def get_status(self, key):
        url = appsettings.ITEM_STATE_PATTERN % (appsettings.MQTT_HOST, key)
        req = requests.get(url)
        self.__success(req)
        return req.text

    def __success(self, req):
        if req.status_code != requests.codes.ok:
            req.raise_for_status()  

