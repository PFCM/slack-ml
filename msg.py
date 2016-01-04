import logging

from flask import Flask
import flask

app = Flask(__name__)

@app.route('/msg/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    msg = flask.request.data['text']
    logging.info('Received message: %s', msg)
    return {'text':msg}
