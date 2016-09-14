from habitica_slack import views


def sync_messages_to_slack():
    from_timestamp = views.get_lastpost_timestamp()
    messages = views.get_messages_from_habitica()
    views.send_messages_to_slack(messages, from_timestamp)
