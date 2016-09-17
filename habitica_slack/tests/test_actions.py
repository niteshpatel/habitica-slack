import json
import os
import time

import requests_mock
from django.test import TestCase

from habitica_slack import actions


class ActionsTestCase(TestCase):
    def setUp(self):
        self.groupId = '123'
        self.apiUser = 'joe'
        self.apiKey = 'secret'

        os.environ['HABITICA_APIUSER'] = self.apiUser
        os.environ['HABITICA_APIKEY'] = self.apiKey
        os.environ['HABITICA_GROUPID'] = self.groupId

    def test_get_lastpost_timestamp(self):
        # arrange
        now_timestamp = (int(time.time()) - (60 * 60 * 24)) * 1000

        # act
        last_post_timestamp = actions.get_lastpost_timestamp()

        # assert
        self.assertEquals(last_post_timestamp, now_timestamp)

    def test_set_lastpost_timestamp(self):
        # arrange
        timestamp = 123

        # act
        actions.set_lastpost_timestamp(timestamp)

        # assert
        last_post_timestamp = actions.get_lastpost_timestamp()
        self.assertEquals(last_post_timestamp, timestamp)

    @requests_mock.mock()
    def test_send_message_to_habitica(self, m):
        # arrange
        data = {
            'user': 'Joe',
            'text': 'Hello!'
        }

        expected_headers = {
            'x-api-user': self.apiUser,
            'x-api-key': self.apiKey,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        m.post(requests_mock.ANY)

        # act
        actions.send_message_to_habitica(data['user'], data['text'])

        # assert
        history = m.request_history
        self.assertEquals(len(history), 1)

        request = history[0]
        self.assertEquals(request.url, 'https://habitica.com/api/v3/groups/123/chat')
        self.assertEquals(request.method, 'POST')
        self.assertDictContainsSubset(expected_headers, request.headers)
        self.assertEquals(request.body, 'message=%5BJoe+says%5D+Hello%21&groupId=123')

    @requests_mock.mock()
    def test_get_messages_from_habitica(self, m):
        # arrange
        expected_headers = {
            'x-api-user': self.apiUser,
            'x-api-key': self.apiKey
        }

        m.get(requests_mock.ANY, text=json.dumps({'data': 'dummy_data'}))

        # act
        response = actions.get_messages_from_habitica()

        # assert
        history = m.request_history
        self.assertEquals(len(history), 1)

        request = history[0]
        self.assertEquals(request.url, 'https://habitica.com/api/v3/groups/123/chat')
        self.assertEquals(request.method, 'GET')
        self.assertDictContainsSubset(expected_headers, request.headers)
        self.assertEquals(request.body, None)

        self.assertEquals(response, 'dummy_data')
