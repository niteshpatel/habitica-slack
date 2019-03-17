import json
import os

import mock
from django.test import TestCase

from habitica_slack import views


class ViewsTestCase(TestCase):
    def setUp(self):
        self.slackToken = 'token'

        os.environ['SLACK_TOKEN'] = self.slackToken

    def test_sync_message_to_habitica_responds_to_invalid_auth_request_with_unauthorized(self):
        # arrange
        dummy_request = create_dummy_post_request()
        dummy_request.body = json.dumps({
            'token': self.slackToken,
            'challenge': 'my_challenge',
            'type': 'arbitrary_event_type',
        })

        views.actions.send_message_to_habitica = mock.Mock()

        # act
        response = views.sync_message_to_habitica(dummy_request)

        # assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, '')

    def test_sync_message_to_habitica_responds_to_valid_url_auth_request_with_ok(self):
        # arrange
        dummy_request = create_dummy_post_request()
        dummy_request.body = json.dumps({
            'token': self.slackToken,
            'challenge': 'my_challenge',
            'type': 'url_verification',
        })

        views.actions.send_message_to_habitica = mock.Mock()

        # act
        response = views.sync_message_to_habitica(dummy_request)

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'text/plain')
        self.assertEqual(response.content, 'my_challenge')

    def test_sync_message_to_habitica_responds_to_invalid_token_with_unauthorized(self):
        # arrange
        user_name = 'Joe'
        text = 'Hello'

        dummy_request = create_dummy_post_request()
        dummy_request.body = json.dumps({
            'token': 'wrong_token',
            'user_name': user_name,
            'text': text
        })

        views.actions.send_message_to_habitica = mock.Mock()

        # act
        response = views.sync_message_to_habitica(dummy_request)

        # assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, '')

    def test_sync_message_to_habitica_with_valid_token_sends_message_to_habitica(self):
        # arrange
        user_name = 'Joe'
        text = 'Hello'

        dummy_request = create_dummy_post_request()
        dummy_request.body = json.dumps({
            'token': self.slackToken,
            'event': {
                'type': 'message',
                'channel': 'my_channel',
                'user': user_name,
                'text': text,
            },
            'type': 'event_callback',
        })

        views.actions.send_message_to_habitica = mock.Mock()

        # act
        response = views.sync_message_to_habitica(dummy_request)

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')
        views.actions.send_message_to_habitica.assert_called_with(user_name, text)

    def test_sync_messages_to_slack(self):
        # arrange
        dummy_request = create_dummy_post_request()
        views.actions.sync_messages_to_slack = mock.Mock(return_value=None)

        # act
        response = views.sync_messages_to_slack(dummy_request)

        # assert
        # noinspection PyUnresolvedReferences
        views.actions.sync_messages_to_slack.assert_called_with()
        self.assertEqual(response.content, '')
        self.assertEqual(response.status_code, 200)

    def test_setup_habitica_webhook(self):
        # arrange
        dummy_request = create_dummy_post_request()
        views.actions.setup_habitica_webhook = mock.Mock(return_value=(200, 'OK'))

        # act
        response = views.setup_habitica_webhook(dummy_request)

        # assert
        # noinspection PyUnresolvedReferences
        views.actions.setup_habitica_webhook.assert_called_with(None)
        self.assertEqual(response.content, 'OK')
        self.assertEqual(response.reason_phrase, 'OK')


def create_dummy_post_request():
    dummy_request = type('', (), {})()
    dummy_request.POST = {}
    dummy_request.build_absolute_uri = lambda path: None

    return dummy_request
