import os
import json
import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def handle_slack_message(request):
    token = request.POST.get('token')
    if token != os.environ['SLACK_TOKEN']:
        return HttpResponse('', status=401)
        
    send_message(
        request.POST.get('user_name'), 
        request.POST.get('text'))
        
    return HttpResponse('', status=200)

    
def send_message(user, text):    
    api_user = os.environ['HABITICA_APIUSER']
    api_key = os.environ['HABITICA_APIKEY']
    group_id = os.environ['HABITICA_GROUPID']
    
    habitica_url = 'https://habitica.com/api/v3/groups/%s/chat' % group_id
       
    headers = {
        'x-api-user': api_user, 
        'x-api-key': api_key
    }    
    data = {
        'groupId': group_id,
        'message': '[%s says] %s' % (user, text)
    }
    
    response = requests.post(habitica_url, headers=headers, data=data)
    