from api.game.image_generator.file_manager import *
from PIL import Image, ImageDraw, ImageFont
from api.game.image_generator.base.image_base import ImageBase

class FarmImage(ImageBase):

    timer = 0

    images = {}

    #Placeholder img; Player enemy and background
    preset_figther_img = ''

    battle_ui_location = ''

    img_battle_stage = ''
    enemy_desc_ui = []

    def __init__(self):

        self.list_img_generated = []

        self.images = [Image.open(x) for x in [
            self.enemy['path-img'],
            self.player['path-img'],
        ]]

        self.img_battle_stage = Image.open(f'{self.PATH_BATTLE_BACKGROUND}{self.zone}{self.PNG_EXT}')   
        
        for i, im in enumerate(self.images, 0):
            self.img_battle_stage.paste(im, (self.fighters_positions[i]["x"], self.fighters_positions[i]["y"]), im)
    
        self.preset_figther_img = self.img_battle_stage

        self.battle_ui_location = {
            'battle_presentation': [
                {"coord": (65, 15),   "text": self.player['name']}, # User name location
                {"coord": (80, 200),  "text": None},                # Player location ui life
                {"coord": (350, 200), "text": None},                # Enemy location ui life
                {"coord": (234, 155), "text": None},                # Current battle round
            ],
            'battle_representation': [ 
                {"coord": (65, 15),   "text": self.player['name']}, # User name location
                {"coord": (80, 200),  "text": None},                # Player location ui life
                {"coord": (350, 200), "text": None},                # Enemy location ui life
                {"coord": (234, 155), "text": None},                # Current battle round
                {"coord": (),         "text": None},                # Variable to location dmg
            ],
            'constant_location': [
                {"coord": (370, 50)},                # Player location ui dmg
                {"coord": (100, 50)},                # Enemy location ui dmg
            ],
            'font': {"font-size": 24, "font-color": (255, 255, 255), "type-font": self.ANTON_FONT}
        }

        self.enemy_desc_ui = {
            'location': [
                {"coord": (112, 102), "text": self.enemy['current-life']},
                {"coord": (112, 129), "text": self.enemy['attack']},
                {"coord": (112, 157), "text": self.enemy['defense']},
            ],
            'font': {"font-size": 24, "font-color": (255, 255, 255), "type-font": self.ANOTHER_ROUND_FONT}
        }
 

    def enemy_desc(self):

        base_img = Image.open(self.enemy['path-profile-img'])

        draw = ImageDraw.Draw(base_img)
        
        font = ImageFont.truetype(self.enemy_desc_ui["font"]["type-font"], size= self.enemy_desc_ui["font"]["font-size"])

        for location in (self.enemy_desc_ui["location"]):
          draw.text(location["coord"], str(location["text"]), font=font)

        return base_img

    def battle_presentation(self):
        
        base_img = self.preset_figther_img.copy()

        draw = ImageDraw.Draw(base_img)

        another_round_26 = ImageFont.truetype(self.battle_ui_location["font"]["type-font"], size= self.battle_ui_location["font"]["font-size"])

        self.battle_ui_location['battle_presentation'][1]['text'] = f"{self.player['current-life']}/{self.player['max-life']}"
        self.battle_ui_location['battle_presentation'][2]['text'] = f"{self.enemy['current-life']}/{self.enemy['max-life']}"
        self.battle_ui_location['battle_presentation'][3]['text'] = f"{self.round}/{self.limit_rounds}"


        for battle_location in self.battle_ui_location['battle_presentation']:
          draw.text(battle_location['coord'], battle_location['text'], font=another_round_26, stroke_fill= self.battle_ui_color['black'], stroke_width=2)

        return base_img

    def battle_representation(self):

        base_img = self.preset_figther_img.copy() 

        draw = ImageDraw.Draw(base_img)

        anton_font_26 = ImageFont.truetype(self.battle_ui_location["font"]["type-font"], size= self.battle_ui_location["font"]["font-size"])

        # Clean UI attack (By turn)
        if self.is_player_turn: 
            if self.is_dodged_attack:
                dmg_taken = "Dogeado"
                self.battle_ui_location['battle_representation'][4]['coord'] = self.battle_ui_location['constant_location'][0]['coord']
            else:
                dmg_taken = f'-{self.enemy["dmg-taken"]}!' if self.is_crit_attack else (f"-{self.enemy['dmg-taken']}" if self.enemy['dmg-taken'] > 0 else 'Mitigado!')
                self.battle_ui_location['battle_representation'][4]['coord'] = self.battle_ui_location['constant_location'][0]['coord']
        else:
            if self.is_dodged_attack:
                dmg_taken = "Dogeado"
                self.battle_ui_location['battle_representation'][4]['coord'] = self.battle_ui_location['constant_location'][1]['coord']
            else:
                dmg_taken = f'-{self.player["dmg-taken"]}!' if self.is_crit_attack else (f"-{self.player['dmg-taken']}" if self.player['dmg-taken'] > 0 else 'Mitigado!')
                self.battle_ui_location['battle_representation'][4]['coord'] = self.battle_ui_location['constant_location'][1]['coord']
        
        self.battle_ui_location['battle_representation'][1]['text'] = f"{self.player['current-life']}/{self.player['max-life']}"
        self.battle_ui_location['battle_representation'][2]['text'] = f"{self.enemy['current-life']}/{self.enemy['max-life']}"
        self.battle_ui_location['battle_representation'][3]['text'] = f"{self.round}/{self.limit_rounds}"
        self.battle_ui_location['battle_representation'][4]['text'] = f"{dmg_taken}"

        for battle_rep_location in self.battle_ui_location['battle_representation']:
          draw.text(battle_rep_location['coord'], battle_rep_location['text'], font=anton_font_26, stroke_fill= self.battle_ui_color['black'], stroke_width=2)

        return base_img

    def post_game(self, reward):

        base_img = {}

        if self.player['current-life'] <= 0:
            base_img = Image.open(self.PATH_LOSE_SCREEN)

        elif self.enemy['current-life'] <= 0:
            
            base_img = Image.open(self.PATH_WIN_SCREEN)
            
            if reward != '': 
                reward_img = Image.open(reward)
                base_img.paste(reward_img, (296, 138), reward_img)

            draw = ImageDraw.Draw(base_img)
            font = ImageFont.truetype(self.ANTON_FONT, 22)
            reward_exp = f"{self.enemy['bounty-exp']}"
            reward_gold = f"{self.enemy['bounty-gold']}"
            draw.text((168, 140), reward_exp, font=font)
            draw.text((168, 183), reward_gold, font=font)

        else:
            base_img = Image.open(self.PATH_DRAW_SCREEN)

        return base_img

    def player_level_up(self, stats_up):
        
        base_image = Image.open(self.PATH_LVL_UP_SCREEN)

        draw = ImageDraw.Draw(base_image)
        font = ImageFont.truetype(self.ANTON_FONT, 22)

        draw.text((138, 173), str(stats_up['life']), font=font)
        draw.text((246, 173), str(stats_up['attack']), font=font)
        draw.text((353, 173), str(stats_up['defense']), font=font)

        return base_image

    def generate_image(self, func_name, *args):

        try:
            function_call = eval('self.' + func_name)
        except NameError:
            print(f"Function '{func_name}' not defined.")
        else:
            if callable(function_call):
                if len(args) > 0:
                    image_path = function_call(*args)
                else: 
                    image_path = function_call()
                self.list_img_generated.append(image_path)
            else:
                print(f"'{func_name}' is not a function.")
                
        