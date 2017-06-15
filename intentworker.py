from luis.luis_response import LUISResponse
from include.intentresolver import *
from include import *
import paho.mqtt.client as mqtt
import json


def find_entity(collection, entity):
    items = [x for x in collection if x.get_type() == entity.typeName and not x.get_name() == None]
    if items and not entity.hasMinScore or (entity.hasMinScore and entity.minScore <= items[0].get_score()):
        return items[0]

def map_parameter(s, dic):
    if s and dic:
        for key in dic.keys():
            s = s.replace("{%s}" % key, dic[key])
    return s

def perform_intent_workflow(luisResponse, intentConfig):
    # Check vality level
    if intentConfig.hasMinScore:
        if intentConfig.minScore > luisResponse.get_top_intent().get_score():
            return False

    # Map entities
    luisParams = { }
    if intentConfig.hasEntities:
        for entity in [x for x in intentConfig.getEntities() if x.isValid]:
            item = find_entity(luisResponse.get_entities(), entity)
            if not item and entity.required:
                return False, entity.missingText
            luisParams.update({ item.get_type(): item.get_name() })

    # Perform Connectors
    if intentConfig.hasConnectors:
        for conn in [x for x in intentConfig.getConnectors() if x.isValid]:
            print conn.target
            payload = json.dumps({ 'luis': luisParams, 'config': conn.parameter })
            client.publish(conn.channel, map_parameter(payload, luisParams))
        
    # Say generic message
    msg = ''
    if intentConfig.message:
        msg = intentConfig.message
        msg = map_parameter(msg, luisParams)
    return True, msg
    
def on_message(client, userdata, msg):  
    try:
        text = str(msg.payload).encode('utf-8')

        response = LUISResponse(text) 
        config = IntentResolver(response.get_top_intent().get_name())
       
        if not config.load() or not config.isValid:
            raise Exception("Error loading intent config")
        
        #logger.info("Performing intent " + config.intent)
        (success, result) = perform_intent_workflow(response, config)
        if result:
            client.publish(appsettings.MQTT_SAY_TOPIC, result)
        elif not success:
            client.publish(appsettings.MQTT_SAY_TOPIC, appsettings.ERROR_TEXT)
    except:
        logger.error("Could not load intent message: " + text, exc_info=True)
        #client.publish(_SAY_TOPIC, "Fehler beim ausfuhren")


def on_connect(client, userdata, flags, rc):
    client.subscribe(appsettings.MQTT_INTENT_TOPIC)
    

logger = applogging.AppLogger("intentworker").instance

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_messag
client.connect(appsettings.MQTT_HOST, 1883, 60)

try: 
    while True:
        client.loop()
except: 
    logger.error("Intent process exception", exc_info=True)

client.disconnect()
del client
del logger