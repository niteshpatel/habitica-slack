import os

import mock
from django.test import TestCase

from habitica_slack import views


class ViewsTestCase(TestCase):
    def setUp(self):
        self.slackToken = 'token'

        os.environ['SLACK_TOKEN'] = self.slackToken

    def test_sync_message_to_habitica_with_valid_token(self):
        # arrange
        user_name = 'Joe'
        text = 'Hello'

        dummy_request = create_dummy_post_request()
        dummy_request.POST = {
            'token': self.slackToken,
            'user_name': user_name,
            'text': text
        }

        views.actions.send_message_to_habitica = mock.Mock()

        # act
        response = views.sync_message_to_habitica(dummy_request)

        # assert
        # noinspection PyUnresolvedReferences
        views.actions.send_message_to_habitica.assert_called_with(user_name, text)
        self.assertEqual(response.content, '')
        self.assertEqual(response.status_code, 200)

    def test_sync_message_to_habitica_with_invalid_token(self):
        # arrange
        dummy_request = create_dummy_post_request()
        dummy_request.POST = {}
        views.actions.send_message_to_habitica = mock.Mock(return_value=None)

        # act
        response = views.sync_message_to_habitica(dummy_request)

        # assert
        # noinspection PyUnresolvedReferences
        views.actions.send_message_to_habitica.assert_not_called()
        self.assertEqual(response.content, '')
        self.assertEqual(response.status_code, 401)

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
        views.actions.setup_habitica_webhook = mock.Mock(return_value=None)

        # act
        response = views.setup_habitica_webhook(dummy_request)

        # assert
        # noinspection PyUnresolvedReferences
        views.actions.setup_habitica_webhook.assert_called_with(None)
        self.assertEqual(response.content, '')
        self.assertEqual(response.status_code, 200)


def create_dummy_post_request():
    dummy_request = type('', (), {})()
    dummy_request.POST = {}
    dummy_request.build_absolute_uri = lambda: None

    return dummy_request
