import hashlib
import hmac
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

    slack_signature = request.META.get('HTTP_X_SLACK_SIGNATURE')
    slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET')
    if slack_signature and slack_signing_secret:
        timestamp = request.META.get('HTTP_X_SLACK_REQUEST_TIMESTAMP', '')
        sig_basestring = 'v0:{0}:{1}'.format(timestamp, request.body)

        my_signature = 'v0={0}'.format(
            hmac.new(slack_signing_secret, sig_basestring, hashlib.sha256).hexdigest()
        )
        if not hmac.compare_digest(my_signature, slack_signature):
            return HttpResponse('invalid signature', status=401)

    token = fields.get('token')
    if token != os.environ['SLACK_TOKEN']:
        return HttpResponse('invalid token', status=401)

    event = fields.get('event')
    if event:
        if event.get('type') == 'message':
            if event.get('channel') != os.environ['SLACK_CHANNEL_ID']:
                return HttpResponse('invalid channel', status=401)

            actions.send_message_to_habitica(
                event.get('user'),
                event.get('text'))
            return HttpResponse('', status=200)

    return HttpResponse('unauthorized request', status=401)


@csrf_exempt
def sync_messages_to_slack(request):
    actions.sync_messages_to_slack()

    return HttpResponse('', status=200)


def setup_habitica_webhook(request):
    status_code, reason_phrase = actions.setup_habitica_webhook(request.build_absolute_uri('/'))

    return HttpResponse(reason_phrase, status=status_code)
