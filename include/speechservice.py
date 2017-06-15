from azuretoken import STSToken
from processhelper import runCommand
import requests
import json
import uuid


class SpeechFunctions:
    _TMP_WAV_FILE = "/tmp/stt.wav"
    
    # -d    Default Device
    # -L    Endian Little
    # -c    Channel (1=Mono)
    # -r    Samplerate
    _REC_CMD  = "sox -d -L -c 1 -r 16000 {0} silence 0 1 0:00:02 5% trim 0 4".format(_TMP_WAV_FILE)

    # 0     Client ID
    # 1     Token
    # 2     Wavefile
    _STT_CMD  = "curl -v -X POST 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=de-DE&format=simple&requestid={0}' " + \
                "-H 'Content-type: audio/wav; codec=\"audio/pcm\"; samplerate=16000' " + \
                "-H 'Transfer-Encoding:chunked' " + \
                "-H 'Authorization: Bearer {1}' " + \
                "--data-binary @{2}"

    # Use program app id
    _LUIS_URL = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/58c6293b-86ff-407c-8642-992dbd1851d4"


    #########################################################################################################################################################################


    def __init__(self, sttKey, luisKey, isDebug = False):
        self.isBusy = False
        self.lastText = None  
        self.isDebug = isDebug
        self.guid = str(uuid.uuid4())
        self.token = STSToken(sttKey)
        self.luisHeader = {
            'Ocp-Apim-Subscription-Key': luisKey,
        }
        
    def recordVoice(self):
        if not self.isBusy:
            try:
                self.isBusy = True
                err, _ = runCommand(self._REC_CMD)
                if err:
                    raise
                self.lastText = None
                return True, self._TMP_WAV_FILE
            finally:
                self.isBusy = False
        return False, None

    def voiceToText(self):
        if not self.isBusy:
            try:
                cmd = self._STT_CMD.format(self.guid, self.token.request(), self._TMP_WAV_FILE)
                _, result = runCommand(cmd)
                if result:   
                    obj = json.loads(result)
                    success = obj['RecognitionStatus'] == "Success"                    
                    if success:
                        self.lastText = obj['DisplayText'].encode('utf-8')
                        return True, self.lastText
                    else:
                        self.lastText = None
            except:
                raise
            finally:
                self.isBusy = False
        return False, None

    def getIntent(self):
        if not self.isBusy and not self.lastText is None:
            try:
                self.isBusy = True
                params = (
                    ('q', self.lastText),
                    ('timezoneOffset', '60'),
                    ('verbose', 'false')
                )
                result = requests.get(self._LUIS_URL, headers=self.luisHeader, params=params)
                if result:
                    return True, result.text
            except:
                raise
            finally:
                self.isBusy = False
        return False, None

    def cleanup(self):
        if not self.isBusy:
            self.token.cleanup()
