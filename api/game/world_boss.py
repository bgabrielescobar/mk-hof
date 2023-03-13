import json
import config.settings as setting
import random
import config.settings as setting
from api.game.image_generator.file_manager import *
from api.game.image_generator.farm_image import *

class Farm(FarmImage):

  round = 0
  limit_rounds = 3
  end_battle = False

  settings = {}
  farm_image = {}

  is_crit_attack = False
  is_dodged_attack = False
  is_player_turn = False

  def __init__(self, player, wb):

    self.player = player
    
    self.generate_wb()

    super().__init__()

  def start(self):

    self.generate_image('enemy_desc')

    self.generate_image('battle_presentation')

    while self.round < self.limit_rounds:
      
      self.round += 1

      self.player, self.enemy = self.battle(self.player, self.enemy)
      
      self.is_player_turn = not self.is_player_turn
      self.generate_image('battle_representation')

      if self.end_battle:
        break;

      self.enemy, self.player = self.battle(self.enemy, self.player)

      self.is_player_turn = not self.is_player_turn
      self.generate_image('battle_representation')

      if self.end_battle:
        break;

    reward = ''
    if self.enemy['current-life'] <= 0:
        reward = self.upgrade_user()

    self.generate_image('post_game', reward)

    return self.generate_resume_battle_gif()
    
    
  def battle(self, attacker, defender):
      self.is_dodge_attack = defender['dodge'] >= random.randint(1, 100);
      if not self.is_dodge_attack: 
        self.is_crit_attack = attacker['crit'] >= random.randint(1, 100);
        calculated_damage = (attacker['attack'] - defender['defense']) * 2 if self.is_crit_attack else attacker['attack'] - defender['defense']
        calculated_damage = calculated_damage if calculated_damage > 0 else 0;
        defender['current-life'] -= calculated_damage if defender['current-life'] >= calculated_damage else defender['current-life']
        defender['dmg-taken'] = calculated_damage

      if defender['current-life'] <= 0:
        self.end_battle = True

      return [attacker, defender]

  def generate_enemy(self):

    self.settings = setting.export_settings()

    enemy_list = self.settings["enemys"][self.zone]
    rune_list = self.settings["rune-list"]

    total_enemys = len(enemy_list) - 1
    
    self.enemy = enemy_list[random.randint(0, total_enemys)]
    
    if self.enemy["rune-drop-rate"] <= random.randint(1, 100): 
      self.enemy['rune-drop'] = '' # No rune drop
    else:
      rune_drop = self.enemy['rune-drop']
      self.enemy['rune-image'] = rune_list[rune_drop]['path-profile']

  def upgrade_user(self):

    user_id = self.player['name']

    users_data = FileManager.get_json(FileManager.USERS_JSON)

    self.player = users_data[user_id]

    self.player['gold'] += self.enemy['bounty-gold']
    self.player['exp'] += self.enemy['bounty-exp']

    rune_img = "";

    if self.enemy['rune-drop']:

      rune = self.enemy['rune-drop']

      if rune in self.player['items']:
        self.player['items'][rune] += 1
      else: 
        self.player['items'][rune] = 1;
      
      rune_img = self.enemy['rune-image']

    user_exp_lv = self.settings["exp-level"][self.player['lv'] - 1] #Get first element from array
    user_class = self.player['class']
    stats_up_class = self.settings["classes"]["lvl_up"][user_class]
    
    if self.player['exp'] >= user_exp_lv:
      self.player['lv'] += 1
      self.player['attack'] += stats_up_class['attack']
      self.player['defense'] += stats_up_class['defense']
      self.player['max-life'] += stats_up_class['life']
      self.player['current-life'] += stats_up_class['life']
      self.generate_image('player_level_up', stats_up_class)

    users_data[user_id] = self.player
    
    with open('api/game/db/users.json', 'w') as file:
      json.dump(users_data, file, indent=4)
    return rune_img

# def update_wb(wb, user_id):
#   with open('api/user/db/world-boss.json', 'r') as file:
#     data = json.load(file)

#   data[wb['name']]['life'] -= data[wb['name']]['life'] - wb['life']
#   data[wb['name']]['participants'].append(user_id)
#   data[wb['name']]['participants-cd'][user_id] = time.mktime((datetime.datetime.now()).timetuple()) * 1000 + 10000