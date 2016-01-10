"""
Contains models for the datastore.
"""
import sys
sys.path.append('~/google-cloud-sdk/lib')

from google.appengine.ext import ndb #pylint: disable=E0401, E0611

class Message(ndb.Model):
    """A single slack message.

    Fields:
        - username (ndb.StringProperty) - the user who posted the message
        - text (ndb.StringProperty) - the text of the message
        - timestamp (ndb.DateTimeProperty) - the date/time the message was
            posted
    """
    username = ndb.StringProperty()
    text = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
