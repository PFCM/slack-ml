"""Tests for maintenance.py"""
import unittest
import random
import time
import datetime
from string import ascii_letters

import webtest

from google.appengine.ext import testbed
from google.appengine.ext import ndb

import maintenance
import models

def random_string(length=10, chars=ascii_letters + ' '):
    """Generate a string of gibberish"""
    return ''.join([random.choice(chars) for _ in range(length)])

def random_record(timestamp=time.time()):
    """Generate a random record with the given time

    Args:
        timestamp (optional[float]) - the timestamp for the record. Default is
            the current time.
    Returns:
        models.Message with random data and the specified timestamp.
    """
    return models.Message(
        username=random_string(),
        text=random_string(50),
        timestamp=datetime.datetime.fromtimestamp(timestamp)
    )

class MaintenanceTest(unittest.TestCase):
    """Does tests"""
    def setUp(self):
        """gets ready to go"""
        reload(maintenance)
        self.testapp = webtest.TestApp(maintenance.app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # set up testbed stubs for ndb
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        """turns off testbed"""
        self.testbed.deactivate()

    def trim_test(self):
        """Ensures it trims the correct number of records
        and trims the correct ones"""
        # first we are going to have to fill up the datastore with
        # some stuff
        for _ in range(10):
            random_record().put()
        # should be 10 in store
        assert models.Message.query().count() == 10
        maintenance.MAX_RECORDS = 5
        maintenance.trim_records(5)
        assert models.Message.query().count() == 5

    def endpoint_test(self):
        """Make sure that the actual handler does the job it is supposed to.
        At this stage this is only trim excess items.
        """
        for _ in range(10):
            random_record().put()
        # should be 10 in store
        assert models.Message.query().count() == 10
        maintenance.MAX_RECORDS = 5
        self.testapp.get('/_maintain')
        assert models.Message.query().count() == 5
