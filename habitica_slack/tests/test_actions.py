import json
import os

import mock
import requests_mock
from django.test import TestCase

from habitica_slack import actions


class ActionsTestCase(TestCase):
    def setUp(self):
        self.groupId = '123'
        self.apiUser = 'joe'
        self.apiKey = 'secret'
        self.slackWebhook = 'http://webhook-url.test/'

        os.environ['HABITICA_APIUSER'] = self.apiUser
        os.environ['HABITICA_APIKEY'] = self.apiKey
        os.environ['HABITICA_GROUPID'] = self.groupId
        os.environ['SLACK_WEBHOOK'] = self.slackWebhook

    def test_get_default_lastpost_timestamp(self):
        # arrange
        now_timestamp = actions.get_timestamp_one_hour_ago()

        # act
        last_post_timestamp = actions.get_lastpost_timestamp()

        # assert
        self.assertEqual(last_post_timestamp, now_timestamp)

    def test_set_lastpost_timestamp(self):
        # arrange
        timestamp = 123

        # act
        actions.set_lastpost_timestamp(timestamp)

        # assert
        last_post_timestamp = actions.get_lastpost_timestamp()
        self.assertEqual(last_post_timestamp, timestamp)

    @requests_mock.mock()
    def test_send_message_to_habitica_from_user(self, m):
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

        expected_url = 'https://habitica.com/api/v3/groups/123/chat'
        expected_body = 'message=%5BJoe+says%5D+Hello%21&groupId=123'

        m.post(requests_mock.ANY)

        # act
        actions.send_message_to_habitica(data['user'], data['text'])

        # assert
        history = m.request_history
        self.assertEqual(len(history), 1)

        request = history[0]
        self.assertEqual(request.url, expected_url)
        self.assertEqual(request.method, 'POST')
        self.assertDictContainsSubset(expected_headers, request.headers)
        self.assertEqual(request.body, expected_body)

    @requests_mock.mock()
    def test_send_message_to_habitica_from_slackbot_does_nothing(self, m):
        # arrange
        data = {
            'user': 'slackbot',
            'text': 'Hello!'
        }

        m.post(requests_mock.ANY)

        # act
        actions.send_message_to_habitica(data['user'], data['text'])

        # assert
        history = m.request_history
        self.assertEqual(len(history), 0)

    @requests_mock.mock()
    def test_send_message_to_habitica_from_other_user_when_in_single_user_mode_does_nothing(self, m):
        # arrange
        os.environ['SINGLE_USER'] = 'me'

        data = {
            'user': 'someone else',
            'text': 'Hello!'
        }

        m.post(requests_mock.ANY)

        # act
        actions.send_message_to_habitica(data['user'], data['text'])

        # assert
        history = m.request_history
        self.assertEqual(len(history), 0)

        # teardown
        del os.environ['SINGLE_USER']

    @requests_mock.mock()
    def test_get_messages_from_habitica(self, m):
        # arrange
        expected_headers = {
            'x-api-user': self.apiUser,
            'x-api-key': self.apiKey
        }

        expected_url = 'https://habitica.com/api/v3/groups/123/chat'

        m.get(requests_mock.ANY, text=json.dumps({'data': 'dummy_data'}))

        # act
        response = actions.get_messages_from_habitica()

        # assert
        history = m.request_history
        self.assertEqual(len(history), 1)

        request = history[0]
        self.assertEqual(request.url, expected_url)
        self.assertEqual(request.method, 'GET')
        self.assertDictContainsSubset(expected_headers, request.headers)
        self.assertEqual(request.body, None)
        self.assertEqual(response, 'dummy_data')

    @requests_mock.mock()
    def test_send_messages_to_slack(self, m):
        # arrange
        messages = [
            {
                'timestamp': 10,
                'text': 'hello from Joe',
                'user': 'Joe'
            },
            {
                'timestamp': 20,
                'text': 'hello from John',
                'user': 'John'
            },
            {
                'timestamp': 30,
                'text': 'hello from ADMIN'
            },
            {
                'timestamp': 40,
                'text': '[emma says] hello from Emma'
            },
            {
                'timestamp': 50,
                'text': 'hello from Emily',
                'user': 'Emily'
            }
        ]

        expected_headers = {
            'content-type': 'application/json'
        }

        expected_post_bodies = [
            {
                "attachments": [
                    {
                        "color": "good",
                        "fields": [
                            {
                                "value": "hello from Emily",
                                "title": "Emily"
                            }
                        ],
                        "fallback": "Emily: hello from Emily"
                    }
                ]
            },
            {
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {
                                "value": "hello from ADMIN", "title": None
                            }
                        ],
                        "fallback": "hello from ADMIN"
                    }
                ]
            },
            {
                "attachments": [
                    {
                        "color": "good",
                        "fields": [
                            {
                                "value": "hello from John",
                                "title": "John"
                            }
                        ],
                        "fallback": "John: hello from John"
                    }
                ]
            }
        ]

        m.post(requests_mock.ANY)

        # act
        actions.send_messages_to_slack(messages, 15)

        # assert
        history = m.request_history
        len_history = len(history)
        self.assertEqual(len_history, 3)

        for i in range(len_history):
            request = history[i]
            self.assertEqual(request.url, self.slackWebhook)
            self.assertEqual(request.method, 'POST')
            self.assertDictContainsSubset(expected_headers, request.headers)
            self.assertEqual(json.loads(request.body), expected_post_bodies[i])

    # noinspection PyMethodMayBeStatic
    def test_sync_messages_to_slack(self):
        # arrange
        expected_timestamp = 3
        expected_messages = [1, 2, 3]

        actions.get_lastpost_timestamp = mock.Mock(return_value=expected_timestamp)
        actions.get_messages_from_habitica = mock.Mock(return_value=expected_messages)
        actions.send_messages_to_slack = mock.Mock()

        # act
        actions.sync_messages_to_slack()

        # assert
        # noinspection PyUnresolvedReferences
        actions.send_messages_to_slack.assert_called_with(expected_messages, expected_timestamp)

    @requests_mock.mock()
    def test_setup_habitica_webhook_checks_for_existing_webhook(self, m):
        # arrange
        expected_headers = {
            'x-api-user': self.apiUser,
            'x-api-key': self.apiKey
        }

        expected_url = 'https://habitica.com/api/v3/user/webhook/123'

        m.put(requests_mock.ANY, text=json.dumps({'success': True}), status_code=200, reason='OK')

        # act
        response = actions.setup_habitica_webhook('http://example.test')

        # assert
        history = m.request_history
        self.assertEqual(len(history), 1)

        request = history[0]
        self.assertEqual(request.url, expected_url)
        self.assertEqual(request.method, 'PUT')
        self.assertDictContainsSubset(expected_headers, request.headers)
        self.assertEqual(request.body, None)
        self.assertEqual(response, (200, 'OK'))

    @requests_mock.mock()
    def test_setup_habitica_webhook_creates_webhook_if_not_present(self, m):
        # arrange
        expected_headers = {
            'x-api-user': self.apiUser,
            'x-api-key': self.apiKey,
            'content-type': 'application/json'
        }

        expected_body = {
            'id': '123',
            'enabled': True,
            'url': 'http://example.test/sync_messages_to_slack',
            'label': 'sync_messages_to_slack',
            'type': 'groupChatReceived',
            'options': {
                'groupId': '123'
            }
        }

        expected_url = 'https://habitica.com/api/v3/user/webhook'

        m.put(requests_mock.ANY, text=json.dumps({'success': False, 'error': 'NotFound'}))
        m.post(requests_mock.ANY, text=json.dumps({'success': True}), status_code=201, reason='Created')

        # act
        response = actions.setup_habitica_webhook('http://example.test/')

        # assert
        history = m.request_history
        self.assertEqual(len(history), 2)

        request = history[1]
        self.assertEqual(request.url, expected_url)
        self.assertEqual(request.method, 'POST')
        self.assertDictContainsSubset(expected_headers, request.headers)
        self.assertEqual(request.body, json.dumps(expected_body))
        self.assertEqual(response, (201, 'Created'))
