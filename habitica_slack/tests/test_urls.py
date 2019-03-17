from django.core.urlresolvers import resolve
from django.test import TestCase


class UrlsTestCase(TestCase):
    def test_sync_message_to_habitica_url_resolves_to_sync_message_to_habitica_view(self):
        # act
        resolver = resolve('/sync_message_to_habitica')

        # assert
        self.assertEqual(resolver.view_name, 'habitica_slack.views.sync_message_to_habitica')

    def test_sync_messages_to_slack_url_resolves_to_sync_messages_to_slack_view(self):
        # act
        resolver = resolve('/sync_messages_to_slack')

        # assert
        self.assertEqual(resolver.view_name, 'habitica_slack.views.sync_messages_to_slack')

    def test_setup_habitica_webhook_url_resolves_to_setup_habitica_webhook_view(self):
        # act
        resolver = resolve('/setup_habitica_webhook')

        # assert
        self.assertEqual(resolver.view_name, 'habitica_slack.views.setup_habitica_webhook')
