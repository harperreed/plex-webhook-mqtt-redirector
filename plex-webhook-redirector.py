#
# Heavily refactored version of the original script to use MQTT instead of HTTP.
# This script is a webhook for Plex that sends MQTT messages to a broker when a media event occurs.
# The script is designed to be run in a Docker container.
# 
# Refactored by Harper Reed (harper@modest.com)
# 
# Original Author: Bailey Belvis (https://github.com/philosowaffle)
#
# Webhook to redirect to other webhooks (ifttt, HA, control4, etc).
# https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks 
#
import os
import json
import logging
from typing import Dict, Any

from flask import Flask, abort, request
import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging Setup
logger = logging.getLogger('plex_webhook_redirector')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: %(message)s')


log_file = os.getenv('LOG_FILE', '/app/logs/plex_webhook_redirector.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug("Starting Plex Webhook Redirector")

# Flask Setup
app = Flask(__name__)
FLASK_PORT = int(os.getenv('FLASK_PORT', '8765'))

# Plex Setup
FILTERED_PLAYERS = os.getenv('TRACKED_PLAYER_UUIDS', '').split(',')
LOCAL_PLAYERS_ONLY = os.getenv('LOCAL_PLAYERS_ONLY', 'true').lower() == 'true'

EVENTS = ['media.play', 'media.pause', 'media.resume', 'media.stop']

# MQTT Setup
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')

def send_mqtt_message(topic: str, message: str) -> None:
    try:
        client = mqtt.Client("P1")
        client.connect(MQTT_BROKER)
        client.publish(topic, message)
        client.disconnect()
        logger.debug(f"MQTT message sent: {message} to topic: {topic}")
    except Exception as e:
        logger.error(f"Failed to send MQTT message: {e}")

def format_webhook_log(webhook: Dict[Any, Any]) -> str:
    try:
        user = webhook['Account']['title']
        event = webhook['event'].split('.')[-1].capitalize()
        device = webhook['Player']['title']
        is_local = "Local" if webhook['Player']['local'] else "Remote"
        
        metadata = webhook['Metadata']
        content_type = metadata['type'].capitalize()
        
        if content_type == 'Episode':
            content = f"{metadata['grandparentTitle']} - S{metadata['parentIndex']:02d}E{metadata['index']:02d} - {metadata['title']}"
        elif content_type == 'Movie':
            content = f"{metadata['title']} ({metadata.get('year', 'N/A')})"
        else:
            content = metadata['title']
        
        log_message = (
            f"Event: {event} | "
            f"User: {user} | "
            f"Content: {content} | "
            f"Device: {device} ({is_local})"
        )
        return log_message
    except KeyError as e:
        return f"Error formatting webhook log: {str(e)}\nRaw webhook: {json.dumps(webhook, indent=2)}"


@app.route("/", methods=['POST'])
def inbound_request():
    
    try:
        data = request.form
        webhook = json.loads(data['payload'])
    except KeyError:
        logger.error("No payload found")
        abort(400)

    log_message = format_webhook_log(webhook)
    logger.info(log_message)

    event = webhook.get('event')
    if not event:
        logger.error("No event found in the json")
        return "No event found in the json", 400

    if event not in EVENTS:
        return 'ok'

    media_type = webhook.get('Metadata', {}).get('type')
    if not media_type:
        logger.error("No media type found in the json")
        return "No media type found in the json", 400

    if media_type not in ["movie", "episode"]:
        logger.debug("Media type was not movie or episode, ignoring.")
        return 'ok'

    if LOCAL_PLAYERS_ONLY:
        is_player_local = webhook.get('Player', {}).get('local', False)
        if not is_player_local:
            logger.info("Not allowed. This player is not local.")
            return 'ok'

    player_uuid = webhook.get('Player', {}).get('uuid')
    if not player_uuid:
        logger.error("No player uuid found")
        return 'ok'

    if FILTERED_PLAYERS and player_uuid not in FILTERED_PLAYERS:
        logger.info(f"{player_uuid} player is not tracked")
        return 'ok'

    message = event.split('.')[-1].capitalize()
    send_mqtt_message(MQTT_TOPIC, message)
    return 'ok'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)
