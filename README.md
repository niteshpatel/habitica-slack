# habitica-slack
Send and receive messages from a Habitica Party Chat to a Slack Channel

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/niteshpatel/habitica-slack)

## Requirements

As well as a Slack channel and a Habitica account, you need to set up an Outgoing WebHook in Slack (see https://slack.com/apps/manage/custom-integrations).  

Integration Settings:
1. Channel: <your-slack-channel> e.g. #Habitica
1. URL: <heroku-app-url>/handle_slack_message e.g. https://myapp.herokuapp.test/handle_slack_message
