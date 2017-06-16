from include.applogging import AppLogger
from include.processhelper import *
from include import *
import paho.mqtt.client as mqtt
import subprocess

def on_message(client, userdata, msg):  
    try:
        text = str(msg.payload).encode('utf-8')
        runCommand(appsettings.SAY_CMD.format(text))
    except:
        logger.error("Could not perform say command", exc_info=True)
 
def on_connect(client, userdata, flags, rc):
    client.subscribe(appsettings.MQTT_SAY_TOPIC)


logger = applogging.AppLogger("sayclient").instance

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(appsettings.MQTT_HOST, 1883, 60)

try: 
    while True:
        client.loop()
except: 
    logger.error("Say process exception", exc_info=True)

client.disconnect()
del client
del logger

