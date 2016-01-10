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
    if flask.request.form['token'] == 'BxXxBTiFbTQI3g9fqtowbMOz' \
        and flask.request.form['user_name'] != USERNAME \
        and flask.request.form['user_name'] != 'slackbot': # avoid feedback
        # send it straight back
        msg = flask.request.form['text']
        logging.info('Received message: "%s" from %s',
                     msg, flask.request.form['user_name'])
        # quickly process it, we want to fail here if things are missing
        msg_data = {
            'username': flask.request.form['user_name'],
            'text': flask.request.form['text'],
            'timestamp': flask.request.form['timestamp']
        }
        # defer handling it
        deferred.defer(data.tools.store_msg, msg_data)
        # return some kind of confirmation
        return json.dumps({'text':random.choice(POSITIVE_RESPONSES)})
    return 'nope', 401
