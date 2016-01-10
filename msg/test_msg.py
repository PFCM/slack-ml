"""Contains tests for the handlers in msg.py"""
import unittest
import time
import json

import webtest

from google.appengine.api import taskqueue
from google.appengine.ext import deferred
from google.appengine.ext import testbed

from . import msg
from data import models


def fake_slack_msg():
    """Creates a false message for testing
    Args:
        none
    Returns:
        a fake message (as a dict)
    """
    return {
        'token':'BxXxBTiFbTQI3g9fqtowbMOz', # probably this should be a secret
        'team_id':'T0001',
        'team_domain':'test',
        'channel_id':'test',
        'timestamp':'{}'.format(time.time()),
        'user_id':'U123456789',
        'user_name':'tester',
        'text':'but African swallows are non-migratory'
    }

class MsgTest(unittest.TestCase):
    """actually does the testing"""
    def setUp(self):
        """Just wraps msg.app in a TestApp"""
        reload(msg) # get a new one each time
        # get the application
        self.testapp = webtest.TestApp(msg.app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        # init taskqueue
        self.testbed.init_taskqueue_stub()
        self.taskqueue_stub = self.testbed.get_stub(
            testbed.TASKQUEUE_SERVICE_NAME)
        # init datastore
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        """deactivates testbed"""
        self.testbed.deactivate()

    def newmsg_test(self):
        """Tests that new msgs are correctly dealt with"""
        resp = self.testapp.post('/new',
                                 params=json.dumps(fake_slack_msg()),
                                 content_type='application/json')
        # make sure that has been deferred properly
        tasks = self.taskqueue_stub.get_filtered_tasks()
        assert len(tasks) == 1
        # make sure it runs
        deferred.run(tasks[0].payload)
        assert len(models.Message.query().fetch(10)) == 1
        # make sure it gave us an appropriate response
        assert resp.json['text'] in msg.POSITIVE_RESPONSES

    def nofeedback_test(self):
        """tests that a request with username `slackbot` should not do anything
        """
        msg = fake_slack_msg()
        msg['user_name'] = 'slackbot'
        resp = self.testapp.post('/new',
                                 params=json.dumps(msg),
                                 content_type='application/json')
        # make sure that has been deferred properly
        tasks = self.taskqueue_stub.get_filtered_tasks()
        assert len(tasks) == 0
