from openhabclient import OpenhabClient
from openhabparam import OpenhabParameter
from include.applogging import AppLogger
from include import *
import paho.mqtt.client as mqtt
import json


def format_result(result, params):
    if params.format:
        result = params.format % float(result)
    if params.type and params.type == "number":
        result = result.replace('.', ',')
    return result

def perform_request(params):
    result = ''

    if "POST" == params.method and params.value:
        openhab.post_command(params.item, params.value)
    elif "PUT" == params.method and params.value:
        openhab.put_status(params.item, params.value)
    elif "GET" == params.method:
        result = openhab.get_status(params.item)
        result = format_result(result, params)

    if params.message:
        output = params.message.format(result)
        client.publish(appsettings.MQTT_SAY_TOPIC, output)


def on_message(client, userdata, msg):  
    try:
        text = str(msg.payload).encode('utf-8')
        data = json.loads(text)
        
        luisParams = data['luis']
        if luisParams:
            # TODO
            # params.type -> edit value
            pass

        configData = data['config']
        if configData:
            params = OpenhabParameter(configData)
            if params.isValid:
                perform_request(params)
            del params
    except:
        logger.error("Could not perform openhab action", exc_info=True)
        
def on_connect(client, userdata, flags, rc):
    client.subscribe(appsettings.OPENHAB_CHANNEL)


openhab = OpenhabClient()
logger = AppLogger("openhab", appsettings.LOG_SUB_PATH).instance

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(appsettings.MQTT_HOST, 1883, 60)

try: 
    while True:
        client.loop()
except: 
    logger.error("Openhab process exception", exc_info=True)

client.disconnect()
del openhab
del client
del logger