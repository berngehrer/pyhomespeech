from include.applogging import AppLogger
from include import *
import paho.mqtt.client as mqtt
import subprocess


def runCommand(command, printError = False):
    status = -1
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = process.communicate() 
    status = process.wait()
    if status == 0:
        return status, output
    elif err:
        raise Exception(err)
    return status, None

def on_connect(client, userdata, flags, rc):
    client.subscribe(appsettings.MQTT_SAY_TOPIC)

def on_message(client, userdata, msg):  
    try:
        text = str(msg.payload).encode('utf-8')
        runCommand(appsettings.SAY_CMD.format(text))
    except:
        logger.error("Could not perform say command", exc_info=True)
    

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

