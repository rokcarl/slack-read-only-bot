import yaml

user_map = {}
channel_map = {}
settings = get_settings()

def get_settings():
  return yaml.load(open("settings.yml").read())

def get_username(user_id):  # gets username by userid
  if user_id in user_map:
    return user_map[user_id]
  username = slack_client.api_call("users.info", user=user_id)['user']['name']
  user_map[user_id] = username
  return username

def get_channel_name(channel_id):  # gets username by userid
  if channel_id in channel_map:
    return channel_map[channel_id]
  channel_name = slack_client.api_call("channels.info", channel=channel_id)["channel"]["name"]
  channel_map[channel_id] = channel_name
  return channel_name

def delete_message_and_notify_user(channel, ts, username):
  print("deleting msg")
  slack_mega_client.api_call("chat.delete", channel=channel, ts=ts)
  slack_client.api_call("chat.postMessage", channel="@{}".format(username), text=settings["delete_msg"])

def check_message(channel, ts, user_id):  # checks if user is authed, if not, deletes
  if get_channel_name(channel) not in settings["read_only_channels"]:
    return
  username = get_username(user_id)
  if username in settings["admin_users"]:
    return
  delete_message_and_notify_user(channel, ts, username)

def parse_slack_output(slack_rtm_output):
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
