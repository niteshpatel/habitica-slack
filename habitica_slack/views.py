import json
import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from habitica_slack import actions


@csrf_exempt
def sync_message_to_habitica(request):
    fields = json.loads(request.body)

    if fields.get('type') == 'url_verification':
        challenge = fields.get('challenge')
        return HttpResponse(challenge, content_type='text/plain', status=200)

    token = fields.get('token')
    if token != os.environ['SLACK_TOKEN']:
        return HttpResponse('', status=401)

    if fields.get('event') and fields['event'].get('type') == 'message':
        event = fields.get('event')
        actions.send_message_to_habitica(
            event.get('user'),
            event.get('text'))
        return HttpResponse('', status=200)

    return HttpResponse('', status=401)


@csrf_exempt
def sync_messages_to_slack(request):
    actions.sync_messages_to_slack()

    return HttpResponse('', status=200)


def setup_habitica_webhook(request):
    status_code, reason_phrase = actions.setup_habitica_webhook(request.build_absolute_uri('/'))

    return HttpResponse(reason_phrase, status=status_code)
