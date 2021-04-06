# Slack read-only bot

Manage your Slack community by making read-only channels. Only admins can post to read-only
channels, other users' messages get deleted and the user gets a message from the bot.

# Setup

## Create the Bot

1. Create a new classic Slack app for your workspace at https://api.slack.com/apps?new_classic_app=1 .
2. Click _App Home_, click the _Add Legacy Bot User_ button, and give your bot a username and name.
2. Click _OAuth & Permissions_ . Under _Scopes_ click _Add an OAuth Scope_ and add the following
   scopes:
     - `bot` - Allow users to interact with the bot (needed to message users)
     - `chat:write:bot` - Allow deleting user messages
3. On the same page click on the _Install App to Workspace_ button and authorize it to connect to
   your workspace. Note that the account that authorizes the bot **must** be able to delete the
   messages of other users. This is usually just the workspace owner/admin.
4. Back on the _OAuth & Permissions_ page, copy the two access tokens (one should start with
   `xoxp-` and the other with `xoxb-`).
5. Invite the bot to all the channels you want to make read-only.

## Run the bot

1. Install the bot using `pip` (`pip install git+https://github.com/pR0Ps/slack-read-only-bot`)
2. Create a config file based on the following example:
```
app_token: xoxp-...
bot_token: xoxb-...
delete_msg: The channel you just posted to is read-only, only admins can post to it.
admins:
  - admin1
  - admin2
channels:
  - channel1
  - channel2
```
4. Run `slack-read-only-bot --config <path to file>` to run the bot and test that it works as expected.
5. [optional] Configure your system to run `slack-read-only-bot` as a service using something like
   `systemd` to ensure that it runs at startup, restarts if it crashes, etc.

# Credits

Based on https://github.com/rokcarl/slack-read-only-bot
