"""
This module handles messages.
"""
import logging
import json
import random

import yaml

from google.appengine.ext import deferred
from google.appengine.api import urlfetch # we've locked in the data so why not

import data.models
import data.tools

from flask import Flask
import flask


app = Flask(__name__)

USERNAME = "ml" # actually its 'slackbot' but docs say this should work, so do both

POSITIVE_RESPONSES = [
    ':yellow_heart:',
    ':smile_cat:',
    'got it',
    'thanks',
    ':black_joker:',
    ':pray:',
    ':unicorn_face:',
    ':godmode:'
]

def get_conf(name):
    """Gets a value out of the secret config file secrets.yaml"""
    # we are just going to read it every time. This is probably unwise
    with open('secrets.yaml') as buf:
        conf = yaml.load(buf)
        return conf[name]


@app.route('/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    # check it's legit
    if flask.request.data:
        msg_data = json.loads(flask.request.data)
    else:
        msg_data = flask.request.form
    if msg_data['token'] == get_conf('outbound_token') \
        and msg_data['user_name'] != USERNAME \
        and msg_data['user_name'] != 'slackbot': # avoid feedback
        msg = msg_data['text']
        logging.info('Received message: "%s" from %s',
                     msg, msg_data['user_name'])
        # quickly process it, we want to fail here if things are missing
        msg_data = {
            'username': msg_data['user_name'],
            'text': msg_data['text'],
            'timestamp': msg_data['timestamp']
        }
        # defer handling it
        deferred.defer(data.tools.store_msg, msg_data)
        # return some kind of confirmation
        return flask.Response(
            json.dumps({'text':random.choice(POSITIVE_RESPONSES)}),
            mimetype='application/json'
            )
    return 'nope'

def format_slackmsg(text):
    return text.replace('\n', '\\n')

@app.route('/post', methods=['POST'])
def post_msg():
    """Posts a message to the webhook in the secret file"""
    webhook_url = get_conf('incoming_webhook')
    # get the message content from the request
    msg_data = json.loads(flask.request.data)
    text = msg_data['text']
    secret = msg_data.get('secret', '')
    if secret != get_conf('post_secret'):
        return 'not allowed', 401
    logging.info('posting: %s', text)
    # make sure the text is appropriately escaped
    body = {
        'text':format_slackmsg(text)
    }
    # use urlfetch to POST it to the webhook
    result = urlfetch.fetch(url=webhook_url,
                            payload=json.dumps(body),
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/json'})
    logging.info('attempted...')
    if result.status_code != 200:
        logging.error('possible issue: %d, %s', result.status_code,
                      result.content)
    else:
        logging.info('...succesfully')
    return '<p>{}, {}</p>'.format(result.status_code, result.content)
