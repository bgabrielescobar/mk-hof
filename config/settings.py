import json

def export_settings():
  with open('config/config.json', 'rb') as file:
    data = json.load(file)
  return data
