"""Looks after the data set, trimming it when necessary etc"""
import logging

from google.appengine.ext import ndb

import models

from flask import Flask
import flask
app = Flask(__name__)

MAX_RECORDS = 5000

@app.route('/_maintain')
def datastore_maintenance():
    """Performs necessary checks on the datastore"""
    logging.info('Beginning datastore mainenance...')
    num_records = models.Message.query().count()
    if num_records > MAX_RECORDS:
        logging.info('  %d records, deleting %d', num_records,
                     num_records-MAX_RECORDS)
        trim_records(num_records - MAX_RECORDS)
    # what else should we check?
    return '<h1>done!</h1>'

def trim_records(num_records):
    """Trims records from the datastore until there are only
    `max_records`. Should remove oldest first.

    Args:
        num_records (int) - the number of the oldest records to delete.
    Returns:
        None
    """
    to_go = models.Message.query().order(-models.Message.timestamp)
    ndb.delete_multi(to_go.fetch(num_records, keys_only=True))
