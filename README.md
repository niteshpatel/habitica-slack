# habitica-slack
Send and receive messages from a Habitica Party Chat to a Slack Channel

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/niteshpatel/habitica-slack)

## Requirements

As well as a Slack channel and a Habitica account, you need to set up (see https://slack.com/apps/manage/custom-integrations):
1. Outgoing WebHook in Slack to forward messages to Habitica
1. Incoming WebHook in Slack to received messages from Habitica

#### Outgoing WebHook Settings
1. Channel: &lt;your-slack-channel&gt; e.g. #Habitica
1. URL: &lt;heroku-app-url&gt;/sync_message_to_habitica e.g. https://myapp.herokuapp.test/sync_message_to_habitica

#### Incoming WebHook Settings
1. Post to Channel: &lt;your-slack-channel&gt; e.g. #Habitica
