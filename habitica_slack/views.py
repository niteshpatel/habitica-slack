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
