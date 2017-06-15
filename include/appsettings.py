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
SAY_CMD             = "pico2wave --lang=de-DE --wave={0} '{1}'; aplay {0}; rm {0}".format(TTS_FILE, "{}")

# Azure
STT_KEY             = "4743d9ad1cbe46f580e6f2dead6fc335"
LUIS_KEY            = "ebda8bd0d24b4e3e9acef00678c518d1"

# Intents
JSON_TEMPLATE       = "intents/%s.json"
ERROR_TEXT          = "Ich habe Sie nicht verstanden"

# Openhab
OPENHAB_CHANNEL     = '/cognitive/speech/channel/openhab'
ITEM_PATTERN        = 'http://%s:8080/rest/items/%s'
ITEM_STATE_PATTERN  = 'http://%s:8080/rest/items/%s/state'
