"""Tools for other people to use the data biz.
"""
import datetime
import models

def store_msg(msg):
    """Actually puts a message into storage. Also checks whether or not there
    are enough messages to do a batch of training and if so, starts that
    process.

    Args:
        msg (dict) - the parsed JSON representing the message
    Returns:
        the ndb key for the added item
    """
    msg['timestamp'] = datetime.datetime.fromtimestamp(float(msg['timestamp']))
    msg_model = models.Message(**msg)
    key =  msg_model.put()
    # how many are there?
    return key
