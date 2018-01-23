import sys
import time
from slackclient import SlackClient


class Bot(object):
  def __init__(self, settings):
    self.settings = settings
    self.user_map = {}
    self.channel_map = {}
    self.socket_delay = 1
    self.slack_client = SlackClient(self.settings["slack_bot_token"])
    self.slack_mega_client = SlackClient(self.settings["mega_token"])
    if not self.slack_client.rtm_connect():
      print("Connection failed. Invalid Slack token?")
      sys.exit(1)
    print("Slack bot connected and running!")

  def get_username(self, user_id):  # gets username by userid
    if user_id in self.user_map:
      return self.user_map[user_id]
    username = self.slack_client.api_call("users.info", user=user_id)['user']['name']
    self.user_map[user_id] = username
    return username

  def get_channel_name(self, channel_id):  # gets username by userid
    if channel_id in self.channel_map:
      return self.channel_map[channel_id]
    channel_name = self.slack_client.api_call("channels.info", channel=channel_id)["channel"]["name"]
    self.channel_map[channel_id] = channel_name
    return channel_name

  def delete_message_and_notify_user(self, channel, ts, username):
    print("deleting msg")
    username = "@{}".format(username)
    self.slack_mega_client.api_call("chat.delete", channel=channel, ts=ts)
    self.slack_client.api_call("chat.postMessage", channel=username, text=self.settings["delete_msg"])

  def check_message(self, channel, ts, user_id):  # checks if user is authed, if not, deletes
    if self.get_channel_name(channel) not in self.settings["read_only_channels"]:
      return
    username = self.get_username(user_id)
    if username in self.settings["admin_users"]:
      return
    self.delete_message_and_notify_user(channel, ts, username)

  def parse_slack_output(self, slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
      for output in output_list:
        if output and "text" in output and "user" in output:
          return output["channel"], output["ts"], output["user"]
        else:
          try:
            if output and "bot_message" in output["subtype"]:
              return output["channel"], output["ts"]
            else:
              break
          except KeyError:
            break

  def run(self):
    while True:
      variables = self.parse_slack_output(self.slack_client.rtm_read())
      if variables and len(variables) == 3:
        try:
          channel, ts, user_id = variables[0], variables[1], variables[2]
          self.check_message(channel, ts, user_id)
        except TypeError:
          continue
      time.sleep(self.socket_delay)

