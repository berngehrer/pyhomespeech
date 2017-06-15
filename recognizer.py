from include.applogging import AppLogger
from include.speechservice import SpeechFunctions
from include import *
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
   
def ButtonInterrupt(channel):
    if gpio.input(channel):     
       try:
           gpio.output(appsettings.REC_PIN, gpio.HIGH)
           success, _ = speech.recordVoice()
           gpio.output(appsettings.REC_PIN, gpio.LOW)
           if not success:        
               logger.debug("Could not record", exc_info=True)       
               return

           success, text = speech.voiceToText()
           if not success:
               logger.debug("Bing STT failed", exc_info=True) 
               client.publish(appsettings.MQTT_SAY_TOPIC, appsettings.ERROR_TEXT)
               return
    
           success, intentJson = speech.getIntent()
           if not success:
               logger.debug("Could not resolve LUIS", exc_info=True) 
               client.publish(appsettings.MQTT_SAY_TOPIC, appsettings.ERROR_TEXT)
    
           if intentJson:
               client.publish(appsettings.MQTT_INTENT_TOPIC, intentJson)
           else:
               client.publish(appsettings.MQTT_SAY_TOPIC, appsettings.ERROR_TEXT)
      
       except:
           logger.warn("Recognition does not work", exc_info=True)
          
                      
gpio.setmode(gpio.BCM)  
gpio.setup(appsettings.BUTTON_PIN, gpio.IN)
gpio.setup(appsettings.REC_PIN, gpio.OUT)
gpio.add_event_detect(appsettings.BUTTON_PIN, gpio.RISING, callback=ButtonInterrupt, bouncetime=250)

logger = applogging.AppLogger("recognizer").instance
speech = speechservice.SpeechFunctions( appsettings.STT_KEY, appsettings.LUIS_KEY )

client = mqtt.Client()
client.connect(appsettings.MQTT_HOST, 1883, 60)

try: 
    while True:
        client.loop()
except: 
    logger.error("Error during recognition", exc_info=True)

gpio.cleanup()
speech.cleanup()
client.disconnect()

del speech
del client
del logger