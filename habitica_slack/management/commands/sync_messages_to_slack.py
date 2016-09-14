from django.core.management.base import BaseCommand

from habitica_slack import actions


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('running sync_messages_to_slack...')
        actions.sync_messages_to_slack()

        self.stdout.write('done.')
