# habitica-slack
Send and receive messages from a Habitica Party Chat to a Slack Channel

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/niteshpatel/habitica-slack)

## Requirements

### Slack Integrations
As well as a Slack channel and a Habitica account, you need to set up (see https://slack.com/apps/manage/custom-integrations):

1. Outgoing WebHook in Slack to forward messages to Habitica
1. Incoming WebHook in Slack to received messages from Habitica

#### Outgoing WebHook Settings
1. Channel: &lt;your-slack-channel&gt; e.g. #Habitica
1. URL: &lt;heroku-app-url&gt;/sync_message_to_habitica e.g. https://myapp.herokuapp.test/sync_message_to_habitica

#### Incoming WebHook Settings
1. Post to Channel: &lt;your-slack-channel&gt; e.g. #Habitica

### Heroku Configuration
Not everything in the Heroku setup can be automated with the Deploy button.  You will need to add the command for the scheduler manually.

1. Browse to https://scheduler.heroku.com/dashboard
1. Add a new job as follows
    1. Command: python manage.py sync_messages_to_slack
    1. Dyno size: Free
    1. Frequency: Every 10 minutes
    