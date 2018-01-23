# Slack read-only bot

Manage your Slack community by making read-only channels. Only admins can post to read-only channels, other users' messages to read-only channels get deleted and the user gets a friendly reminder from the bot.

# For Slack Admins

1. Create new bot: https://my.slack.com/services/new/bot, username e.g.: `friendly-bot`.
2. Send over two API tokens to sysadmin. One should start with `xoxb-` and the other with `xoxp-`.
3. Invite bot to all the read-only channels.

# For Sysadmin

1. Create a server and SSH to it.
2. Initialize the system
```
sudo apt update
sudo apt install -y python3-pip
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
```
4. Run the bot.
```
python3 main.py &
```
