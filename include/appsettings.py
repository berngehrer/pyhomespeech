# Logging
LOG_PATH            = 'log/error.log'
LOG_SUB_PATH        = '../log/error.log'
LOG_FORMAT          = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# MQTT
MQTT_HOST           = '192.168.178.69'
MQTT_SAY_TOPIC      = '/cognitive/action/speech/say'
MQTT_INTENT_TOPIC   = '/cognitive/action/speech/intent'

# Voice Recording
BUTTON_PIN          = 17
REC_PIN             = 27
TTS_FILE            = '/tmp/tts.wav'
STT_FILE            = "/tmp/stt.wav"
SAY_CMD             = "pico2wave --lang=de-DE --wave={0} '{1}'; aplay {0}; rm {0}".format(TTS_FILE, "{}")
# -d    Default Device
# -L    Endian Little
# -c    Channel (1=Mono)
# -r    Samplerate
REC_CMD             = "sox -d -L -c 1 -r 16000 {0} silence 0 1 0:00:02 4% trim 0 4".format(STT_FILE)

# Azure
STT_KEY             = "4743d9ad1cbe46f580e6f2dead6fc335"
LUIS_KEY            = "ebda8bd0d24b4e3e9acef00678c518d1"

# 0     Client ID
# 1     Token
# 2     Wavefile
STT_CMD             = "curl -v -X POST 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=de-DE&format=simple&requestid={0}' " + \
                      "-H 'Content-type: audio/wav; codec=\"audio/pcm\"; samplerate=16000' " + \
                      "-H 'Transfer-Encoding:chunked' " + \
                      "-H 'Authorization: Bearer {1}' " + \
                      "--data-binary @{2}"

# Use program app id
LUIS_URL            = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/58c6293b-86ff-407c-8642-992dbd1851d4"

# Intents
JSON_TEMPLATE       = "intents/%s.json"
ERROR_TEXT          = "Ich habe Sie nicht verstanden"

# Openhab
OPENHAB_CHANNEL     = '/cognitive/speech/channel/openhab'
ITEM_PATTERN        = 'http://%s:8080/rest/items/%s'
ITEM_STATE_PATTERN  = 'http://%s:8080/rest/items/%s/state'
