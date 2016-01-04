import logging
import json

from flask import Flask
import flask

app = Flask(__name__)

USERNAME = "ml" # username of bot on slack

@app.route('/msg/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    # check it's legit
    if flask.request.form['token'] == 'BxXxBTiFbTQI3g9fqtowbMOz' \
        and flask.request.form['user_name'] != USERNAME: # avoid feedback
        # send it straight back
        msg = flask.request.form['text']
        logging.info('Received message: %s', msg)
        return json.dumps({'text':msg})
    return 'nope', 401
