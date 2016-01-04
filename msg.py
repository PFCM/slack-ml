import logging
import json

from flask import Flask
import flask

app = Flask(__name__)

USERNAME = "ml" # actually its 'slackbot' but docs say this should work, so do both

@app.route('/msg/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    # check it's legit
    if flask.request.form['token'] == 'BxXxBTiFbTQI3g9fqtowbMOz' \
        and flask.request.form['user_name'] != USERNAME \
        and flask.request.form['user_name'] != 'slackbot': # avoid feedback
        # send it straight back
        msg = flask.request.form['text']
        logging.info('Received message: "%s" from %s', msg, flask.request.form['user_name'])
        return json.dumps({'text':msg})
    return 'nope', 401
