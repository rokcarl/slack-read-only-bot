import yaml


def get_settings():
  return yaml.load(open("settings.yml").read())
