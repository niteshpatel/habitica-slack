# habitica-slack [![Build Status](https://img.shields.io/travis/niteshpatel/habitica-slack.svg)](https://travis-ci.org/niteshpatel/habitica-slack) [![Code Climate](https://img.shields.io/codeclimate/maintainability/niteshpatel/habitica-slack.svg)](https://codeclimate.com/github/niteshpatel/habitica-slack) [![Coverage](https://img.shields.io/codeclimate/coverage-letter/niteshpatel/habitica-slack.svg)](https://codeclimate.com/github/niteshpatel/habitica-slack) [![License](https://img.shields.io/github/license/niteshpatel/habitica-slack.svg?maxAge=3600)](https://raw.githubusercontent.com/niteshpatel/habitica-slack/master/LICENSE.txt) [![StackShare](http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](http://stackshare.io/niteshpatel/habitica-slack)
[Habitica extension](http://habitica.wikia.com/wiki/Slack_Chat_Integration) to send and receive messages from a Habitica Group Chat to a Slack Channel.  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/niteshpatel/habitica-slack)

## Requirements

### Slack Integrations
As well as a Slack channel and a Habitica account, you need to [create a slack app to manage message delivery](https://api.slack.com/slack-apps#creating_apps):

1. Setup Event Subscriptions in Slack to support sending messages from Slack to Habitica
1. Setup Incoming WebHooks in Slack to support receiving messages from Habitica to Slack

#### Setup Event Subscriptions in Slack
1. Browse to Event Subscriptions
1. Enable Events: On
1. Request URL: &lt;heroku-app-url&gt;/sync_message_to_habitica e.g. https://myapp.herokuapp.test/sync_message_to_habitica
1. Subscribe to Workspace Events > Add Workspace Event: message.channels
1. Subscribe to Workspace Events > Add Workspace Event: message.groups

#### Setup Incoming WebHooks in Slack
1. Browse to Incoming Webhooks
1. Activate Incoming Webhooks: On
1. Webhook URLs for Your Workspace > Add New Webhook to Workspace: Post to: &lt;your-slack-channel&gt; e.g. #Habitica

### Setup Habitica WebHook
1. Visit &lt;heroku-app-url&gt;/setup_habitica_webhook to setup the Habitica webhook

### Heroku Configuration (optional if Habitica WebHook above is not working)
Not everything in the Heroku setup can be automated with the Deploy button.  You will need to add the command for the scheduler manually.

1. Browse to https://scheduler.heroku.com/dashboard
1. Add a new job as follows
    1. Command: python manage.py sync_messages_to_slack
    1. Dyno size: Free
    1. Frequency: Every 10 minutes
    