import datetime
import yaml


def get_settings():
  return yaml.load(open("settings.yml").read())

def log(msg, level="info"):
  print(msg)
  with open("log.txt", "a") as f:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write("{}: {}\n".format(ts, msg))
