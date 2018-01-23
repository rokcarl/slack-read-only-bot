import bot
import sys
import time
from slackclient import SlackClient


settings = bot.get_settings()
slack_client = SlackClient(settings["slack_bot_token"])
slack_mega_client = SlackClient(settings["mega_token"])


socket_delay = 1
if not slack_client.rtm_connect():
  print("Connection failed. Invalid Slack token?")
  sys.exit(1)
print("DeleteBot connected and running!")
while True:
  variables = bot.parse_slack_output(slack_client.rtm_read())
  if variables and len(variables) == 3:
    try:
      channel, ts, user_id = variables[0], variables[1], variables[2]
      bot.check_message(channel, ts, user_id)
    except TypeError:
      continue
  time.sleep(socket_delay)
