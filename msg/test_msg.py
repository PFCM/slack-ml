"""Contains tests for the handlers in msg.py"""
import unittest
import time
import json

import webtest

from google.appengine.api import taskqueue
from google.appengine.ext import deferred
from google.appengine.ext import testbed

from google.appengine.api import apiproxy_stub
from google.appengine.api import apiproxy_stub_map

from . import msg
from data import models

class URLFetchMock(apiproxy_stub.APIProxyStub):
    """Mocks google.appengine.api.urlfetch, just returns whatever it is told to
    This is almost entirely thanks to Jeff Rebeiro:

    http://blog.rebeiro.net/2012/03/mocking-appengines-urlfetch-service-in.html
    """
    def __init__(self, service_name='urlfetch'):
        super(URLFetchMock, self).__init__(service_name)

    def set_return_values(self, **kwargs):
        """Determines what the 'request' will return"""
        self.return_values = kwargs

    def _Dynamic_Fetch(self, request, response):
        """Make the false response"""
        rvs = self.return_values # for brevity's sake
        response.set_content(rvs.get('content', ''))
        response.set_statuscode(rvs.get('status_code', 200))
        for header_key, header_val in rvs.get('headers', {}).items():
            header = response.add_header()
            header.set_key(header_key)
            header.set_value(header_val)
        response.set_finalurl(rvs.get('final_url', request.url()))
        response.set_contentwastruncated(
            rvs.get('content_was_truncated', False))
        self.request = request
        self.response = response


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
        # make sure that has been not deferred properly
        tasks = self.taskqueue_stub.get_filtered_tasks()
        assert len(tasks) == 0

class PostTest(unittest.TestCase):
    """Tests (or attempts to test) that messages can be posted approps."""
    def setUp(self):
        """Just wraps msg.app in a TestApp, inits stubs necessary"""
        reload(msg) # get a new one each time
        # get the application
        self.testapp = webtest.TestApp(msg.app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        # init mock urlfetch
        self.urlfetch_mock = URLFetchMock()
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', self.urlfetch_mock)

    def tearDown(self):
        """deactivates testbed"""
        self.testbed.deactivate()

    def test_post(self):
        """Overall test, runs the handler and hopes to get a success status
        code"""
        secret = msg.get_conf('post_secret')
        # make the request body
        body = {'secret': secret, 'text':'test'}
        # set the response from the fake urlfetch
        self.urlfetch_mock.set_return_values(content='neat')
        # make the request
        resp = self.testapp.post('/post',
                                 params=json.dumps(body),
                                 content_type='/application/json')
        self.assertEqual(200, resp.status_code)

    def test_noauth(self):
        """Test to see if we get a 401 when we omit the secret"""
        # make the request body
        body = {'text':'test'}
        # set the response from the fake urlfetch
        self.urlfetch_mock.set_return_values(content='neat')
        # make the request
        try:
            resp = self.testapp.post('/post',
                                     params=json.dumps(body),
                                     content_type='/application/json')
        except webtest.AppError as e:
            assert '401' in str(e)
        else:
            assert False # make sure the exception is in fact thrown, else fail

    def test_postfailed(self):
        """Test to see that it returns appropriate response when it fails to
        post a message"""
        secret = msg.get_conf('post_secret')
        # make the request body
        body = {'secret': secret, 'text':'test'}
        # set the response from the fake urlfetch
        self.urlfetch_mock.set_return_values(content='nope', status_code=500)
        # make the request
        resp = self.testapp.post('/post',
                                 params=json.dumps(body),
                                 content_type='/application/json')
        print(resp.body)
        assert '<p>500, nope</p>' == resp.body
