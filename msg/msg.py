"""
This module handles messages.
"""
import logging
import json
import random

from google.appengine.ext import deferred

import data.models

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

@app.route('/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    # check it's legit
    logging.info('new message. hi')
    logging.info('data: %s', flask.request.data)
    if flask.request.data:
        msg_data = json.loads(flask.request.data)
    else:
        msg_data = flask.request.form
    for key in msg_data:
        logging.info('{}:{}'.format(key, msg_data[key]))
    if msg_data['token'] == 'BxXxBTiFbTQI3g9fqtowbMOz' \
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
