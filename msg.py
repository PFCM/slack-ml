import logging

from flask import Flask
import flask

app = Flask(__name__)

@app.route('/msg/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    # check it's legit
    if flask.request.data['token'] == 'BxXxBTiFbTQI3g9fqtowbMOz':
        msg = flask.request.data['text']
        logging.info('Received message: %s', msg)
        return {'text':msg}
    return 'nope', 401
