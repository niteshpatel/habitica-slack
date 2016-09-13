import os
import json
import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_slack_message(request):
    send_message(
        request.POST.get('user_name'), 
        request.POST.get('text'))
    
    return HttpResponse(request.body)
    
    
def send_message(user, text):
    group_id = os.environ['HABITICA_GROUPID']
    
    habitica_url = 'https://habitica.com/api/v3/groups/%s/chat' % group_id
    
    api_user = os.environ['HABITICA_APIUSER']
    api_key = os.environ['HABITICA_APIKEY']
    
    headers = {
        'x-api-user': api_user, 
        'x-api-key': api_key
    }
    
    data = {
        'groupId': group_id,
        'message': text
    }
    
    response = requests.post(habitica_url, headers=headers, data=data)
    