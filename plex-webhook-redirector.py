#
# Author: Bailey Belvis (https://github.com/philosowaffle)
#
# Webhook to redirect to other webhooks (ifttt, HA, control4, etc).
# https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks 
#
import os
import sys
import json
import logging
import hashlib
import shutil
import requests

from flask import Flask, abort, request
import paho.mqtt.client as mqtt
from random import shuffle


print "o yea"

import config_helper as config

##############################
# Logging Setup
##############################

if config.ConfigSectionMap("LOGGER")['logfile'] is None:
  logger.error("Please specify a path for the logfile.")
  sys.exit(1)



logger = logging.getLogger('plex_webhook_redirector')
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: %(message)s')

# File Handler
file_handler = logging.FileHandler(config.ConfigSectionMap("LOGGER")['logfile'])
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug("Starting Plex Webhook Redirector:)")

##############################
# Flask Setup
##############################
flask_port = int(config.ConfigSectionMap("SERVER")['flaskport'])

upload_folder = os.getcwd() + '/tmp'

if flask_port is None:
  logger.info("Using default Flask Port: 5000")
  flask_port = 5000

flask_debug = False

##############################
# Plex Setup
##############################
plex_config = config.ConfigSectionMap("PLEX")


filtered_players = [] if plex_config['trackedplayeruuids'] == "none" else plex_config['trackedplayeruuids'].split(',')

logger.debug("Filtered Players: " + filtered_players.__str__())

local_players_only = True if plex_config['localplayersonly'] is None else plex_config['localplayersonly']  

events = [
  'media.play',
  'media.pause',
  'media.resume',
  'media.stop'
]

##############################
# Helper Methods
##############################

def send_mqtt_message(topic, message):
  broker = config.ConfigSectionMap("MQTT")['broker']
  client = mqtt.Client("P1") #create new instance
  client.connect(broker) #connect to broker
  client.publish(topic,message) #publish
  client..disconnect()

##############################
# Server
##############################
app = Flask(__name__)

@app.route("/", methods=['POST'])
def inbound_request():
  # read the json webhook
  data = request.form

  try:
    webhook = json.loads(data['payload'])
  except:
    logger.error("No payload found")
    abort(400)

  logger.debug(webhook)

  # Extract the event
  try:
    event = webhook['event']
    logger.info("Event: " + event)
  except KeyError:
    logger.error("No event found in the json")
    return "No event found in the json"

  # Only perform action for event play/pause/resume/stop for TV and Movies
  if not event in events:
    # Take no action
    return 'ok'

     # Extract the media type
  try:
       media_type = webhook['Metadata']['type']
       logger.debug("Media Type: " + media_type)
  except KeyError:
    logger.error("No media type found in the json")
    return "No media type found in the json"

  if (media_type != "movie") and (media_type != "episode"):
    logger.debug("Media type was not movie or episode, ignoring.")
    return 'ok'

  # Unless we explicitly said we want to enable remote players, 
    # Let's filter events
  if local_players_only:
    is_player_local = True # Let's assume it's true
    try:
      is_player_local = webhook['Player']['local']
      logger.debug("Local Player: " + is_player_local.__str__())
    except Exception as e:
      logger.info("Not sure if this player is local or not :(")
      logger.debug("Failed to parse [Player][local] - " + e.__str__())
    if not is_player_local:
      logger.info("Not allowed. This player is not local.")
      return 'ok'

  try:
    player_uuid = webhook['Player']['uuid'].__str__()
    logger.debug("Player UUID: " + player_uuid)
  except:
    logger.error("No player uuid found")
    return 'ok'

  # If we configured only specific players to be able to play with the lights
  if filtered_players:
    try:
      if player_uuid not in filtered_players:
        logger.info(player_uuid + " player is not tracked")
        return 'ok'
    except Exception as e:
      logger.error("Failed to check uuid - " + e.__str__())


  topic = config.ConfigSectionMap("MQTT")['topic']
  
  if event == 'media.stop':
    # HANDLE STOP
    logger.debug("Sending 'stop' message to " + config.ConfigSectionMap("MQTT")['topic'])
    #r = requests.get(config.ConfigSectionMap("WEBHOOKS")['mediastopwebhook'])
    send_mqtt_message(topic,"Stop") #publish
    return 'ok'

  if event == 'media.pause':
    # HANDLE PAUSE
    logger.debug("Sending 'pause' message to " + config.ConfigSectionMap("MQTT")['topic'])
    #r = requests.get(config.ConfigSectionMap("WEBHOOKS")['mediapausewebhook'])
    send_mqtt_message(topic,"Pause") #publish
    return 'ok'

  if event == 'media.play':

    # HANDLE PLAY OR RESUME
    logger.debug("Sending 'play' message to " + config.ConfigSectionMap("MQTT")['topic'])
    #r = requests.get(config.ConfigSectionMap("WEBHOOKS")['mediaplaywebhook'])
    send_mqtt_message(topic,"Play") #publish
    return 'ok'

  if event == 'media.resume':
    # HANDLE RESUKE
    logger.debug("Sending 'resume' message to " + config.ConfigSectionMap("MQTT")['topic'])
    #r = requests.get(config.ConfigSectionMap("WEBHOOKS")['mediaresumewebhook'])
    
    send_mqtt_message(topic,"Resume") #publish
    return 'ok'

if __name__ == "__main__":

  
  app.run(host='0.0.0.0', port=flask_port, debug=flask_debug)

