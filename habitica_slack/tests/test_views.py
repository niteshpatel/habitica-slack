import json
import os

import mock
from django.test import TestCase

from habitica_slack import views


class ViewsTestCase(TestCase):
    def setUp(self):
        self.slackToken = 'token'

        os.environ['SLACK_TOKEN'] = self.slackToken
        os.environ['SLACK_CHANNEL_ID'] = 'my_channel'

    def test_sync_message_to_habitica_with_invalid_challenge_returns_unauthorized(self):
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
        self.assertEqual(response.content, 'unauthorized request')

    def test_sync_message_to_habitica_with_valid_challenge_returns_ok(self):
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

    def test_sync_message_to_habitica_with_invalid_token_returns_unauthorized(self):
        # arrange
        user_name = 'Joe'
        text = 'Hello'

        dummy_request = create_dummy_post_request()
        dummy_request.body = json.dumps({
            'token': 'wrong_token',
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
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'invalid token')

    def test_sync_message_to_habitica_with_invalid_channel_returns_unauthorized(self):
        # arrange
        user_name = 'Joe'
        text = 'Hello'

        dummy_request = create_dummy_post_request()
        dummy_request.body = json.dumps({
            'token': self.slackToken,
            'event': {
                'type': 'message',
                'channel': 'wrong_channel',
                'user': user_name,
                'text': text,
            },
            'type': 'event_callback',
        })

        views.actions.send_message_to_habitica = mock.Mock()

        # act
        response = views.sync_message_to_habitica(dummy_request)

        # assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'invalid channel')

    def test_sync_message_to_habitica_with_valid_token_returns_ok_and_sends_message(self):
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

    def test_sync_messages_to_slack_returns_ok(self):
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

    def test_setup_habitica_webhook_returns_ok(self):
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
