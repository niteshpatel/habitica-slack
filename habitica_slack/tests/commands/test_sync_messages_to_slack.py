import os

import mock
from django.test import TestCase

from habitica_slack.management.commands import sync_messages_to_slack


class SyncMessagesToSlackTestCase(TestCase):
    def setUp(self):
        self.slackToken = 'token'

        os.environ['SLACK_TOKEN'] = self.slackToken

    # noinspection PyMethodMayBeStatic
    def test_sync_message_to_habitica_with_valid_token(self):
        # arrange
        original = sync_messages_to_slack.actions.sync_messages_to_slack
        sync_messages_to_slack.actions.sync_messages_to_slack = mock.Mock()

        # act
        sync_messages_to_slack.Command().handle()

        # assert
        # noinspection PyUnresolvedReferences
        sync_messages_to_slack.actions.sync_messages_to_slack.assert_called_with()

        # cleanup
        sync_messages_to_slack.actions.sync_messages_to_slack = original
