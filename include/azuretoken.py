import requests
import time
import os

class STSToken:
    _TOKEN_FILE = "azure.token"
    _ENDPOINT   = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"

    # key = subscription key
    # caching_time = minutes until renew token
    def __init__(self, key, caching_time = 9):
        self.header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': key,
        }
        self.caching_time = caching_time * 60

    def __del__(self):
        if self.__fileExists():
            os.remove(self._TOKEN_FILE)

    def request(self):
        if not self.__fileExists() or self.__isFileDeprecated():
            r = requests.post(self._ENDPOINT, headers=self.header)
            self.__write(r.text)
        return self.__read()

    def __read(self):        
        f = open(self._TOKEN_FILE, "r")
        token = f.read()
        f.close()
        return token

    def __write(self,token):
        f = open(self._TOKEN_FILE, "w")
        f.write(token)
        f.close()

    def __fileExists(self):
        return os.path.exists(self._TOKEN_FILE)

    def __isFileDeprecated(self):
        delta = time.time() - os.path.getmtime(self._TOKEN_FILE)
        return delta > self.caching_time
