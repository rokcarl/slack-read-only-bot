#!/usr/bin/env python

import argparse
import functools
import logging
import time

from slackclient import SlackClient
from slackclient.exceptions import SlackClientError
import yaml


__log__ = logging.getLogger(__name__)
LOG_LEVELS = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)


def api_call(client, *args, **kwargs):
    """Wrap SlackClient.api_call so it raises errors when something goes wrong"""
    ret = client.api_call(*args, **kwargs)
    if not ret.get("ok"):
        raise SlackClientError(ret.get("error", "[unknown error]"))
    return ret


class ReadOnlyBot:
    def __init__(self, *, bot_token, app_token, delete_msg, admins, channels):
        self.delete_msg = delete_msg
        self.admins = set(admins or [])
        self.channels = set(channels or [])

        # Log in and check the tokens worked (note that this doesn't mean they
        # have the required scopes)
        self.slack_bot = SlackClient(bot_token)
        if not self.slack_bot.rtm_connect():
            raise Exception("Bot RTM connection failed. Invalid Slack bot token?")

        self.slack_app = SlackClient(app_token)
        try:
            api_call(self.slack_app, "auth.test")
        except SlackClientError as e:
            raise Exception("App failed to authenticate. Invalid Slack app token?") from e

        __log__.info("Slack bot connected and running!")

    @functools.lru_cache(maxsize=None)
    def get_username(self, user_id):
        return api_call(self.slack_bot, "users.info", user=user_id)["user"]["name"]

    @functools.lru_cache(maxsize=None)
    def get_channel_name(self, channel_id):
        return api_call(self.slack_bot, "conversations.info", channel=channel_id)["channel"]["name"]

    def delete_message(self, channel_id, ts):
        try:
            api_call(self.slack_app, "chat.delete", channel=channel_id, ts=ts)
        except SlackClientError as e:
            __log__.error(
                "Failed to delete message from #%s: %s",
                self.get_channel_name(channel_id), e
            )

    def message_user(self, user_id, text):
        try:
            api_call(
                self.slack_bot,
                "chat.postMessage",
                channel="@{}".format(self.get_username(user_id)),
                text=text
            )
        except SlackClientError as e:
            __log__.error("Failed to send message to %s: %s", username, e) 

    def process_event(self, event):
        """Process an individual event from Slack"""
        if not event or "text" not in event:
            return

        channel_id = event.get("channel")
        ts = event.get("ts")
        user_id = event.get("user")
        if not (channel_id and ts and user_id):
            return

        # Check if message is in a read-only channel and from a non-admin
        if (
            self.get_channel_name(channel_id) not in self.channels or
            self.get_username(user_id) in self.admins
        ):
            return

        # Delete the message and PM the user
        __log__.info(
            "Deleting message from @%s to #%s",
            self.get_username(user_id),
            self.get_channel_name(channel_id)
        )

        self.delete_message(channel_id, ts)
        if self.delete_msg:
            self.message_user(user_id, self.delete_msg)

    def run(self):
        while True:
            for event in self.slack_bot.rtm_read():
                self.process_event(event)

            # Avoid uselessly spinning the CPU
            time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="A Slack bot that makes channels read-only")
    parser.add_argument(
        "-c", "--config",
        help="The config file to use",
        type=argparse.FileType(mode='rt'),
        required=True
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Increase log verbosity for each occurence up to 4 (default: ERROR)",
        action="count",
        default=0
    )
    args = parser.parse_args()


    # Set the log level
    __log__.setLevel(LOG_LEVELS[min(3, max(0, args.verbose))])
    ReadOnlyBot(**yaml.safe_load(args.config.read())).run()


if __name__ == "__main__":
    main()
