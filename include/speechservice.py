from azuretoken import STSToken
from processhelper import runCommand
from include import appsettings
import requests
import json
import uuid

class SpeechFunctions:

    def __init__(self, sttKey, luisKey):
        self._isBusy = False
        self._lastText = 'Licht aus' # None  
        self._guid = str(uuid.uuid4())
        self._token = STSToken(sttKey)
        self._luisHeader = {
            'Ocp-Apim-Subscription-Key': luisKey,
        }
        
    def recordVoice(self):
        if not self._isBusy:
            try:
                self._isBusy = True
                err, _ = runCommand(appsettings.REC_CMD)
                if err:
                    raise 
                self._lastText = None
                return True, appsettings.STT_FILE
            finally:
                self._isBusy = False
        return False, None

    def voiceToText(self):
        if not self._isBusy:
            try:
                cmd = appsettings.STT_CMD.format(self._guid, self._token.request(), appsettings.STT_FILE)
                _, result = runCommand(cmd)
                if result:   
                    obj = json.loads(result)
                    success = obj['RecognitionStatus'] == "Success"                    
                    if success:
                        self._lastText = obj['DisplayText'].encode('utf-8')
                        return True, self._lastText
                    else:
                        self._lastText = None
            except:
                raise
            finally:
                self._isBusy = False
        return False, None

    def getIntent(self):
        if not self._isBusy and not self._lastText is None:
            try:
                self._isBusy = True
                params = (
                    ('q', self._lastText),
                    ('timezoneOffset', '60'),
                    ('verbose', 'false')
                )
                result = requests.get(appsettings.LUIS_URL, headers=self._luisHeader, params=params)
                if result:
                    return True, result.text
            except:
                raise
            finally:
                self.isBusy = False
        return False, None

    def cleanup(self):
        if not self._isBusy:
            self._token.cleanup()

