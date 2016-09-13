from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_slack_message(request):
    return HttpResponse(request.body)
    