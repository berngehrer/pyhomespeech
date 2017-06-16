from azuretoken import STSToken
from applogging import AppLogger
from processhelper import runCommand
import appsettings
import requests
import json
import uuid

class SpeechFunctions:

    def __init__(self, sttKey, luisKey):
        self._lastText = None
        self._guid = str(uuid.uuid4())
        self._token = STSToken(sttKey)
        self._luisHeader = {
            'Ocp-Apim-Subscription-Key': luisKey,
        }
        self._logger = AppLogger("speech", file=appsettings.LOG_SUB_PATH).instance
        
    def recordVoice(self):
        try:
            err, _ = runCommand(appsettings.REC_CMD)
            if err:
                raise 
            self._lastText = None
            return True, appsettings.STT_FILE
        except:
            self._logger.error("Recording error", exc_info=True)
        return False, appsettings.STT_FILE
    
    def voiceToText(self):
        try:
            cmd = appsettings.STT_CMD.format(self._guid, self._token.request(), appsettings.STT_FILE)
            err, result = runCommand(cmd)
            if err:
                raise
            if result:   
                obj = json.loads(result)
                success = obj['RecognitionStatus'] == "Success"                    
                if success:
                    self._lastText = obj['DisplayText'].encode('utf-8')
                    return True, self._lastText
                else:
                    self._lastText = None
        except:
            self._logger.error("STT error", exc_info=True)
        return False, ''

    def getIntent(self):
        try:
            params = (
                ('q', self._lastText),
                ('timezoneOffset', '60'),
                ('verbose', 'false')
            )
            result = requests.get(appsettings.LUIS_URL, headers=self._luisHeader, params=params)
            if result:
                return True, result.text
        except:
            self._logger.error("LUIS error", exc_info=True)
        return False, ''

    def cleanup(self):
        if not self._isBusy:
            self._token.cleanup()
