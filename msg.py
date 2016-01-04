import logging
import json

from flask import Flask
import flask

app = Flask(__name__)

lastmsg = ""

@app.route('/msg/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    # check it's legit
    if flask.request.form['token'] == 'BxXxBTiFbTQI3g9fqtowbMOz':
        # send it straight back
        msg = flask.request.form['text']
        if msg != lastmsg:
            logging.info('Received message: %s', msg)
            # lol avoid feedback loop
            lastmsg = msg
            return json.dumps({'text':msg})
    return 'nope', 401
