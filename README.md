# Slack read-only bot

Manage your Slack community by making read-only channels. Only admins can post to read-only channels, other users' messages to read-only channels get deleted and the user gets a friendly reminder from the bot.

# For Slack Admins

1. Create a new app: https://api.slack.com/slack-apps.
2. Go to _Bot Users_ in the navigation and click on the _Add a Bot User_. Enter e.g. `friendly-bot` and save.
3. Go to _OAuth & Permissions_ in the navigation of the app. Under _Scopes_ select the _Send messages as user_ (`chat:write:user`) permission and click on _Save Changes_.
4. On the same page click on the _Install App to Workspace_ button and _authorize_ on the next screen.
5. You are presented with access tokens. Send over two API tokens to the sysadmin. One should start with `xoxb-` and the other with `xoxp-`.

# For Sysadmin

1. Create a server and SSH to it.
2. Initialize the system
```
sudo apt update
sudo apt install -y python3-pip monit
pip3 install slackbot
sudo chown ubuntu /srv
cd /srv
git clone https://gitlab.com/rokcarl/slack-read-only-bot.git
cd slack-read-only-bot
```
3. Configure settings.
```
cp settings.yml.example settings.yml
vim settings.yml
cp monitrc ~/.monitrc
```
4. Run monit that will run the bot.
```
monit
```
