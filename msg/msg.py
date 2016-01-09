"""
This module handles messages.
"""
import logging
import json
import random

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

def store_msg(msg):
    """Actually puts a message into storage. Also checks whether or not there
    are enough messages to do a batch of training and if so, starts that
    process.

    Args:
        msg (str) - the message to store
    Returns:
        None
    """
    pass

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
        # defer handling it
        return json.dumps({'text':random.choice(POSITIVE_RESPONSES)})
    return 'nope', 401
