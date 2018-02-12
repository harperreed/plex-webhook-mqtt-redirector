# plex-webhook-redirector
A webhook for Plex that changes the color of your LIFX lights to match the main colors of the poster art being played.

## Requirements
- Plex Pass and Server version that supports [Plex Webhooks](https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks)
- Python 2.7 (has not been verified with Python 3)
- Clone Repository


## Usage
- Navigate to directory where you cloned the repository
- [Configure variables](#configuration) - must restart script after any config changes
- pip install -r requirements.txt
- `python plex_webhook_redirector.py`
- Add the webhook `http://localhost:5000` to your Plex Server

## How it works
This webhook runs a local webserver using [Flask](http://flask.pocoo.org/) which recieves requests from Plex when certain media events occur for categories `movie` and `episode`.  Based on filter criteria that can be set in the config file the webhook decides whether or not to generate an effect.  If this event matches our criteria then it sends a webhook to your specific event webhook


