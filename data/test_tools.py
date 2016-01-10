"""Tests for functions provided by tools.py"""
from contextlib import contextmanager
import time

from nose import with_setup

import tools
import models

from google.appengine.ext import ndb
from google.appengine.ext import testbed

@contextmanager
def ndb_context():
    tb_obj = testbed.Testbed()
    tb_obj.activate()
    tb_obj.init_datastore_v3_stub()
    tb_obj.init_memcache_stub()
    # clear cache
    ndb.get_context().clear_cache()
    # yield the testbed
    yield tb_obj
    # cleanup
    tb_obj.deactivate()

def get_msg():
    """Creates a false message for testing.

    Args:
        none
    Returns:
        dict - contains all the fields necessary for store_msg
    """
    return {
        'username': 'test_man',
        'text': 'a test message',
        'timestamp': '{}'.format(time.time())
    }

def test_store_msg():
    """Ensures we can store a message"""
    with ndb_context():
        tools.store_msg(get_msg())
        assert len(models.Message.query().fetch(10)) == 1
