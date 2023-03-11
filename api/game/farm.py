import random
import json
import config.settings as setting
from PIL import Image
from api.game.manager.file_manager import *
from PIL import Image, ImageDraw, ImageFont
from api.game.manager.image_manager import *

class Farm:

  round = 0
  limit_rounds = 3
  end_battle = False

  image_manager = {}

  player = {}
  enemy = {}

  is_crit_attack = False
  is_dodged_attack = False

  def start(self, user_id, type):

    users_data = FileManager.get_json(FileManager.USERS_JSON)
    
    if user_id not in users_data:
        return "assets/mermeid.jpg"
    
    self.player = users_data[user_id]

    self.generate_enemy(type)

    self.image_manager = ImageManager(self.player, self.enemy, type)

    self.image_manager.generate_image('self.enemy_desc', self.player, self.enemy)
    
    # BATTLE GAME LOOP
    self.image_manager.generate_image('self.battle_presentation', self.player, self.enemy)

    while self.round < self.limit_rounds:
      
      self.round += 1

      self.player, self.enemy = self.battle(self.player, self.enemy)
      
      is_player_turn = True
      self.image_manager.generate_image('self.battle', self.player, self.enemy, self.is_crit_attack, self.is_dodged_attack, is_player_turn, str(self.round))

      if self.end_battle:
        break;

      self.enemy, self.player = self.battle(self.enemy, self.player)

      is_player_turn = False
      self.image_manager.generate_image('self.battle', self.player, self.enemy, self.is_crit_attack, self.is_dodged_attack, is_player_turn, str(self.round))

      if self.end_battle:
        break;

    reward = ''
    if self.enemy['current-life'] <= 0:
        reward = self.upgrade_user(user_id)

    self.image_manager.generate_image('self.post_game', self.player, self.enemy, reward)

    return self.image_manager.generate_resume_battle_gif(user_id)
    
    
  def battle(self, attacker, defender):
      self.is_crit_attack = attacker['crit'] >= random.randint(1, 100);
      calculated_damage = (attacker['attack'] - defender['defense']) * 2 if self.is_crit_attack else attacker['attack'] - defender['defense']
      calculated_damage = calculated_damage if calculated_damage > 0 else 0;
      defender['current-life'] -= calculated_damage if defender['current-life'] >= calculated_damage else defender['current-life']
      defender['dmg-taken'] = calculated_damage

      if defender['current-life'] <= 0:
        self.end_battle = True

      return [attacker, defender]

  def generate_enemy(self, type):

    enemy_list = setting.export_settings("enemys")[type]
    rune_list = setting.export_settings("rune-list")

    total_enemys = len(enemy_list) - 1
    
    self.enemy = enemy_list[random.randint(0, total_enemys)]
    
    if self.enemy["rune-drop-rate"] + 100 <= random.randint(1, 100): 
      self.enemy['rune-drop'] = '' # No rune drop
    else:
      self.enemy['rune-image'] = rune_list[self.enemy['rune-drop']]['path-profile']

  def upgrade_user(self, user_id):
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

    user_exp_lv = setting.export_settings("exp-level")[self.player['lv'] - 1] #Get first element from array

    if self.player['exp'] >= user_exp_lv:
      self.player['lv'] += 1
      self.player['attack'] += 1
      self.player['defense'] += 2
      self.player['max-life'] += 3
      self.player['current-life'] += 3
      stats_up = {"attack": 1, "defense": 2, "life": 3}
      self.image_manager.generate_image('self.player_level_up', self.player, self.enemy, stats_up)

    users_data[user_id] = self.player
    
    with open('api/game/db/users.json', 'w') as file:
      json.dump(users_data, file, indent=4)
    return rune_img