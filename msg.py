import logging

from flask import Flask
import flask

app = Flask(__name__)

@app.route('/msg/new', methods=['POST'])
def new_msg():
    """Stores new messages"""
    # check it's legit
    if flask.request.form['token'] == 'BxXxBTiFbTQI3g9fqtowbMOz':
        # send it straight back
        msg = flask.request.form['text']
        logging.info('Received message: %s', msg)
        return {'text':msg}
    return 'nope', 401
