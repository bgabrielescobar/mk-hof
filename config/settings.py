import json

def export_settings(key_setting):
  with open('config/config.json', 'rb') as file:
    data = json.load(file)
  return data[key_setting]
