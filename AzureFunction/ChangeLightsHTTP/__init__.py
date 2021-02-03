import logging
import os
import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Lights trigger received message:' + str(req.get_body()))

    valueDel = "</at>"

    registry_manager = IoTHubRegistryManager(os.environ["IoTHubConnection"])
    
    effect = req.params.get('effect')
    if not effect:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            fullText = req_body.get('text')
            effect = fullText[fullText.index(valueDel) + len(valueDel):].replace('&nbsp;', ' ').strip()
    
    if not isAnEffect(effect): 
        effect = "help"

    if effect == "help" :
        return func.HttpResponse(formatReply("Try passing one of these: \n bpm  \n candy cane   \n confetti   \n cyclon rainbow   \n dots   \n fire   \n glitter   \n juggle   \n lightning  \n noise   \n police all   \n police one   \n rainbow   \n rainbow with glitter  \n ripple   \n sinelon   \n solid   \n twinkle  "), 
        status_code=200) 
    if effect :
        registry_manager.send_c2d_message(os.environ["deviceId"], effect, properties={})

        return func.HttpResponse(formatReply(f"You chose {effect}. The lights should be changing."), status_code=200)
    
def formatReply(msg: str):
    return '{    "type": "message",    "text": "' + msg + '" }'

def isAnEffect(input: str) :
    effects = [
    "bpm",
    "candy cane",  
    "confetti",  
    "cyclon rainbow",  
    "dots",  
    "fire",  
    "glitter",  
    "juggle",  
    "lightning",
    "noise",  
    "police all",  
    "police one",  
    "rainbow",  
    "rainbow with glitter", 
    "ripple",  
    "sinelon",  
    "solid",  
    "twinkle"
    ]
    return input in effects