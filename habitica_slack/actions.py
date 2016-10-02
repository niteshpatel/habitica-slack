import json
import os
import requests
import time

from habitica_slack import models


def sync_messages_to_slack():
    from_timestamp = get_lastpost_timestamp()
    messages = get_messages_from_habitica()
    send_messages_to_slack(messages, from_timestamp)


def set_lastpost_timestamp(time_stamp):
    models.LastPostTimeStamp.objects.all().delete()

    last_post_time_stamp = models.LastPostTimeStamp()
    last_post_time_stamp.time_stamp = time_stamp
    last_post_time_stamp.save()


def get_lastpost_timestamp():
    last_post_time_stamp = models.LastPostTimeStamp.objects.first()
    if not last_post_time_stamp:
        last_post_time_stamp = models.LastPostTimeStamp()

        time_stamp = get_timestamp_one_hour_ago()
        last_post_time_stamp.time_stamp = time_stamp
        last_post_time_stamp.save()

    return last_post_time_stamp.time_stamp


def send_message_to_habitica(user, text):
    if user.lower() == 'slackbot':
        return

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

    requests.post(habitica_url, headers=headers, data=data)


def get_messages_from_habitica():
    group_id = os.environ['HABITICA_GROUPID']

    habitica_url = 'https://habitica.com/api/v3/groups/%s/chat' % group_id

    api_user = os.environ['HABITICA_APIUSER']
    api_key = os.environ['HABITICA_APIKEY']

    headers = {
        'x-api-user': api_user,
        'x-api-key': api_key
    }

    response = requests.get(habitica_url, headers=headers)
    return response.json()['data']


def send_messages_to_slack(messages, from_timestamp):
    slack_url = os.environ['SLACK_WEBHOOK']

    last_timestamp = None
    for m in reversed(messages):
        if m['timestamp'] <= from_timestamp:
            continue

        last_timestamp = m['timestamp']

        if m['text'].startswith('['):
            continue

        headers = {
            'content-type': 'application/json'
        }

        payload = build_payload(m, m.get('user'))

        requests.post(slack_url, headers=headers, data=json.dumps(payload))

    if last_timestamp:
        set_lastpost_timestamp(last_timestamp)


def setup_habitica_webhook(url_host):
    group_id = os.environ['HABITICA_GROUPID']

    habitica_url = 'https://habitica.com/api/v3/user/webhook/%s' % group_id

    api_user = os.environ['HABITICA_APIUSER']
    api_key = os.environ['HABITICA_APIKEY']

    headers = {
        'x-api-user': api_user,
        'x-api-key': api_key,
        'content-type': 'application/json'
    }

    response = requests.put(habitica_url, headers=headers)
    data = response.json()

    if data['success'] == False and data['error'] == 'NotFound':
        habitica_url = 'https://habitica.com/api/v3/user/webhook'

        data = {
            'id': os.environ['HABITICA_GROUPID'],
            'enabled': True,
            'url': '%ssync_messages_to_slack' % url_host,
            'label': 'sync_messages_to_slack',
            'type': 'groupChatReceived',
            'options': {
                'groupId': os.environ['HABITICA_GROUPID']
            }
        }

        response = requests.post(habitica_url, headers=headers, json=data)

    return (response.status_code, response.reason)


def build_payload(m, user):
    payload = {
        'attachments': [
            {
                'fallback': (user and (user + ': ') or '') + m['text'],
                'color': user and 'good' or 'danger',
                'fields': [
                    {
                        'title': user,
                        'value': m['text']
                    }
                ]
            }
        ]
    }

    return payload


def get_timestamp_one_hour_ago():
    return (int(time.time()) - (60 * 60 * 24)) * 1000
