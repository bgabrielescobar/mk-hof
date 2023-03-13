import random
import json
import imageio
import glob
#from api.game.manager.file_manager import *
#from api.game.manager.image_manager import *
from PIL import Image

class PVP:

    attacker_user = {}
    rival_user = {}

    round = 0
    limit_rounds = 3
    end_duel = False

    def start(self, user_id, duel_user_id):
        
        if user_id == duel_user_id:
            return "No puedes luchar contigo."

        users_data = FileManager.get_json(FileManager.USERS_JSON)
        
        self.attacker_user = users_data[user_id] 
        self.rival_user = users_data[duel_user_id]

        self.equip_items_players()

        self.generate_img_rival_description()

        return self.users_duel()


    def users_duel(self):
        print('TODO')
        #while self.attacker_user["current-life"] > 0 and self.rival_user["current-life"] > 0 and self.round < self.limit_rounds:
      
        #    self.round += 1

        #    self.attacker_user, self.rival_user = self.battle( self.attacker_user, self.rival_user)

            #self.generate_battle_img(user_id)

        #    if self.end_duel:
        #        return f"Cumeado {self.rival_user['name']}"

        #    self.attacker_user, self.rival_user = self.battle(self.rival_user,  self.attacker_user)

            #self.generate_battle_img(user_id)

        #    if self.end_duel:
        #        return f"Cumeado {self.attacker_user['name']}"

    def battle(self, attacker, defender):

        calculated_damage = (attacker['attack'] - defender['defense'])  
        calculated_damage = calculated_damage if calculated_damage > 0 else 0;
        defender['current-life'] -= calculated_damage

        if defender['current-life'] <= 0:
            self.end_duel = True
            return [attacker, defender]

        
         #battle_details += f"Vida restante de {defender['name']} es \u001b[0;33m{defender['life']}\u001b[0;0m\n"
        return [attacker, defender]        

    def equip_items_players(self):

        for item in self.attacker_user['items']:
            self.attacker_user['attack'] += item['attack']
            self.attacker_user['defense'] += item['defense']
            #self.attacker_user['current-life'] += item['life']

        for item in self.rival_user['items']:
            self.rival_user['attack'] += item['attack']
            self.rival_user['defense'] += item['defense']
            #self.rival_user['current-life'] += item['life']
