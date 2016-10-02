import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from habitica_slack import actions


@csrf_exempt
def sync_message_to_habitica(request):
    token = request.POST.get('token')
    if token != os.environ['SLACK_TOKEN']:
        return HttpResponse('', status=401)

    actions.send_message_to_habitica(
        request.POST.get('user_name'),
        request.POST.get('text'))

    return HttpResponse('', status=200)


@csrf_exempt
def sync_messages_to_slack(request):
    actions.sync_messages_to_slack()

    return HttpResponse('', status=200)


def setup_habitica_webhook(request):
    status_code, reason_phrase = actions.setup_habitica_webhook(request.build_absolute_uri('/'))

    return HttpResponse(reason_phrase, status=status_code)
