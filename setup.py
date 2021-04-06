#!/usr/bin/env python

from setuptools import setup

setup(
    name="slack-read-only-bot",
    version="0.0.1",
    description="Make Slack channels read-only by restricting which users can post to them",
    url="https://github.com/pR0Ps/slack-read-only-bot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires = [
        "slackclient>=1.1.0,<2.0.0",
        "pyyaml>=5.4.1,<6.0.0",
    ],
    py_modules=["slack_read_only_bot"],
    entry_points={"console_scripts": ["slack-read-only-bot=slack_read_only_bot:main"]},
)
