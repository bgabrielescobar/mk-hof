import random
import json
import config.settings as setting
import datetime
import time

def farm_wb(user_id, wb):

  player = get_player(user_id)
  enemy = generate_wb(wb)
  
  ms = datetime.datetime.now()
  formated_ms = time.mktime(ms.timetuple()) * 1000
  # USER CAN ATTACK WB
  if user_id in enemy['participants-cd'] and enemy['participants-cd'][user_id] > formated_ms:
    return "Aun no puedes atacar!"
  
  battle_details = "```ansi"

  # BATTLE GAME LOOP

  battle_details += f"\n[2;37m{user_id} vs {enemy['name']}[0m\n\n"
  
  battle_details += f"\n[2;37mNivel: {enemy['lv']}[0m\n\n"

  battle_details += ""

  LIMIT_ROUNDS = 5
  round = 0
    
  player = equip_player_items(player)


  while player["life"] > 0 and enemy["life"] > 0 and round < LIMIT_ROUNDS:
    
    round += 1

    player, enemy, battle_details, end_battle = battle(player, enemy, battle_details)
    if end_battle:
      break;
    enemy, player, battle_details, end_battle = battle(enemy, player, battle_details)
    if end_battle:
      break;

  update_wb(enemy, user_id)

  if enemy['life'] <= 0:
    # To Do Bounty
    battle_details += f"\nRecompensa:\n\u001b[0;33mOro\u001b[0;0m: 0\n\u001b[0;35mExp\u001b[0;0m: 0 ```"
    #upgrade_user(user_id, enemy['bounty-gold'], enemy['bounty-exp'])
    return battle_details

  if player['life'] <= 0:  
    battle_details += f"\n\u001b[0;33mPerdiste\u001b[0;0m```"
    return battle_details
  
  battle_details += f"\n\u001b[0;33m{enemy['name']} Huyó\u001b[0;0m```"
  
  return battle_details

def battle(attacker, defender, battle_details):
    calculated_damage = (attacker['attack'] - defender['defense'])  
    calculated_damage = calculated_damage if calculated_damage > 0 else 0;
    defender['life'] -= calculated_damage

    battle_details += f"{attacker['name']} ataca y hace un daño total de: \u001b[0;31m{calculated_damage}\u001b[0;0m\n"

    if defender['life'] <= 0:
      battle_details += f"\u001b[0;31m{defender['name']} a sido abatido\u001b[0;0m\n"
      return [attacker, defender, battle_details, 1]

      
    battle_details += f"Vida restante de {defender['name']} es \u001b[0;33m{defender['life']}\u001b[0;0m\n"
    return [attacker, defender, battle_details, 0]

def update_wb(wb, user_id):
  with open('api/user/db/world-boss.json', 'r') as file:
    data = json.load(file)

  data[wb['name']]['life'] -= data[wb['name']]['life'] - wb['life']
  data[wb['name']]['participants'].append(user_id)
  data[wb['name']]['participants-cd'][user_id] = time.mktime((datetime.datetime.now()).timetuple()) * 1000 + 10000

  with open('api/user/db/world-boss.json', 'w') as file:
    json.dump(data, file)

def generate_wb(name_wb):

  wb = get_wb(name_wb)

  wb['name'] = name_wb
  wb["lv"] = "NULL"

  return wb

def upgrade_user(user_id, gold, exp):
  with open('api/user/db/users.json', 'r') as file:
    data = json.load(file)

  data[user_id]['gold'] += gold
  data[user_id]['exp'] += exp

  user_exp_lv = setting.export_settings("exp-level")[data[user_id]['lv'] - 1] #Get first element from array

  if data[user_id]['exp'] >= user_exp_lv:
    data[user_id]['lv'] += 1
    data[user_id]['attack'] += 5
    data[user_id]['defense'] += 5
    data[user_id]['life'] += 5
    

  with open('api/user/db/users.json', 'w') as file:
    json.dump(data, file)

def get_player(user_id):
  with open('api/user/db/users.json', 'r') as file:
    data = json.load(file)
  return data[user_id]

def get_wb(wb_name):
  with open('api/user/db/world-boss.json', 'r') as file:
    data = json.load(file)
  return data[wb_name]

def equip_player_items(player):

  for item in player['items']:
    player['attack'] += item['attack']
    player['defense'] += item['defense']
    player['life'] += item['life']

  return player
