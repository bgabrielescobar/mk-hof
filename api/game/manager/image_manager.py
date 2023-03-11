import config.settings as setting
from api.game.manager.file_manager import *
from PIL import Image, ImageDraw, ImageFont
from api.game.manager.base.image_base import ImageBase

class ImageManager(ImageBase):

    images = {}

    # Coordenates to render player and enemy on battle stage
    fighters_positions = [
            {"x":300, "y": 50}, # Enemy
            {"x":60, "y": 50},  # Player
    ]

    battle_ui_location = {
        "user_coord_name": (75, 15),   # User name location
        "player_text_dmg": (370, 50),  # Player location ui dmg
        "player_ui_life" : (80, 200),  # Player location ui life
        "enemy_text_dmg":  (100, 50),  # Enemy location ui dmg
        "enemy_ui_life":   (350, 200), # Enemy location ui life
        "coord_dmg_text":  (),         # Variable to location dmg
        "round_battle":    (234, 155),
    }

    battle_ui_color = {
        "red_color": (255, 95, 95),
        "black":     (0, 0, 0)
    }

    battle_background_path = ''
    coord_ui_profile_text = []

    def __init__(self, player, enemy, type):
        self.images = [Image.open(x) for x in [
            enemy['path-tiny-img'],
            player['path-img'],
        ]]

        self.coord_ui_profile_text = [
            {"x": 30, "y": 70, "text": enemy['name'], "font-size": 30, "font-color": (194, 235, 167), "type-font": self.ANOTHER_ROUND_FONT},
            {"x": 70, "y": 118, "text": enemy['current-life'], "font-size": 20, "font-color": (255, 255, 255), "type-font": self.ANOTHER_ROUND_FONT},
            {"x": 160, "y": 117, "text": enemy['attack'], "font-size": 20, "font-color": (255, 255, 255), "type-font": self.ANOTHER_ROUND_FONT},
            {"x": 112, "y": 145, "text": enemy['defense'], "font-size": 20, "font-color": (255, 255, 255), "type-font": self.ANOTHER_ROUND_FONT},
        ]  

        # Set default Battle background
        type = 1 if isinstance(type, int) else type

        self.battle_background_stage = Image.open(f'assets/ui/battle_background_{type}.png')   

    def battle(self, player, enemy, is_crit_attack, is_dodged_attack, is_player_turn, round):

        base_img = self.battle_background_stage.copy() # Get background stage

        for count, im in enumerate(self.images, 0):
            base_img.paste(im, (self.fighters_positions[count]["x"], self.fighters_positions[count]["y"]), im)

        draw = ImageDraw.Draw(base_img)

        font = ImageFont.truetype(self.ANTON_FONT, 26)

        # Clean UI attack (By turn)
        if is_player_turn : 
            dmg_taken = f'-{enemy["dmg-taken"]}!' if is_crit_attack else (f"-{enemy['dmg-taken']}" if enemy['dmg-taken'] > 0 else 'Mitigado!')
            self.battle_ui_location['coord_dmg_text'] = self.battle_ui_location['player_text_dmg']

        else :
            dmg_taken = f'-{player["dmg-taken"]}!' if is_crit_attack else (f"-{player['dmg-taken']}" if player['dmg-taken'] > 0 else 'Mitigado!')
            self.battle_ui_location['coord_dmg_text'] = self.battle_ui_location['enemy_text_dmg']
        
        player_ui_life, enemy_ui_life = [f"{player['current-life']}/{player['max-life']}", f"{enemy['current-life']}/{enemy['max-life']}"] 

        # Render damage (player or enemy)
        draw.text(self.battle_ui_location['coord_dmg_text'], dmg_taken, fill= self.battle_ui_color['red_color'], font=font, stroke_fill= (0, 0, 0), stroke_width=2)

        # Render player name
        draw.text(self.battle_ui_location['user_coord_name'], player['name'], font=font, stroke_fill= self.battle_ui_color['black'] ,stroke_width=2)

        round_battle = round + "/3"

        draw.text(self.battle_ui_location['round_battle'], round_battle, font=font, stroke_fill= self.battle_ui_color['black'] ,stroke_width=2)

        draw.text(self.battle_ui_location["player_ui_life"], player_ui_life, font=font)
        draw.text(self.battle_ui_location["enemy_ui_life"], enemy_ui_life, font=font)

        return base_img

    def enemy_desc(self, player, enemy):
        
        base_img = Image.open(enemy['path-profile-img'])

        enemy_img = Image.open(enemy['path-tiny-img'])

        base_img.paste(enemy_img, (250, 50), enemy_img)

        draw = ImageDraw.Draw(base_img)
        
        for i in range(len(self.coord_ui_profile_text)):
          font = ImageFont.truetype(self.coord_ui_profile_text[i]["type-font"], size= self.coord_ui_profile_text[i]["font-size"])
          draw.text(
            ( 
              self.coord_ui_profile_text[i]["x"],
              self.coord_ui_profile_text[i]["y"]
            ),
              str(self.coord_ui_profile_text[i]["text"]),
              fill=self.coord_ui_profile_text[i]["font-color"],
              font=font,
            )

        return base_img

    def battle_presentation(self, player, enemy):
        
        base_img = self.battle_background_stage.copy() # Get background stage

        for count, im in enumerate(self.images, 0):
            base_img.paste(im, (self.fighters_positions[count]["x"], self.fighters_positions[count]["y"]), im)

        draw = ImageDraw.Draw(base_img)

        font_anton_26 = ImageFont.truetype(self.ANTON_FONT, 26)

        player_ui_life = f"{player['current-life']}/{player['max-life']}"
        enemy_ui_life = f"{enemy['current-life']}/{enemy['max-life']}"

        draw.text(self.battle_ui_location['user_coord_name'], player['name'], font=font_anton_26, stroke_fill= self.battle_ui_color['black'] ,stroke_width=2)
        draw.text(self.battle_ui_location["player_ui_life"], player_ui_life, font=font_anton_26)
        draw.text(self.battle_ui_location["enemy_ui_life"], enemy_ui_life, font=font_anton_26)

        return base_img

    def post_game(self, player, enemy, reward):

        base_img = {}

        if player['current-life'] <= 0:
            base_img = Image.open('assets/ui/lose_screen.png')

        elif enemy['current-life'] <= 0:
            
            base_img = Image.open('assets/ui/victory_screen.png')
            
            if reward != '': 
                reward_img = Image.open(reward)
                base_img.paste(reward_img, (296, 138), reward_img)

            draw = ImageDraw.Draw(base_img)
            font = ImageFont.truetype(self.ANTON_FONT, 22)
            reward_exp = f"{enemy['bounty-exp']}"
            reward_gold = f"{enemy['bounty-gold']}"
            draw.text((168, 140), reward_exp, font=font)
            draw.text((168, 183), reward_gold, font=font)

        else:
            base_img = Image.open('assets/ui/draw_screen.png')

        return base_img

    def player_level_up(self, player, enemy, stats_up):
        
        base_image = Image.open('assets/player/lvl_up.png')

        draw = ImageDraw.Draw(base_image)
        font = ImageFont.truetype(self.ANTON_FONT, 22)

        draw.text((138, 179), str(stats_up['life']), font=font)
        draw.text((246, 179), str(stats_up['attack']), font=font)
        draw.text((353, 179), str(stats_up['defense']), font=font)

        return base_image

    def generate_image(self, func_name, player, enemy, *args):
                
        self.total_images += 1

        try:
            function_call = eval(func_name)
        except NameError:
            print(f"Function '{func_name}' not defined.")
        else:
            if callable(function_call):
                if len(args) > 0:
                    image_path = function_call(player, enemy, *args)
                else: 
                    image_path = function_call(player, enemy)
                image_path.save(f"api/game/db/cache/farm/{player['name']}-{self.total_images}.png")
            else:
                print(f"'{func_name}' is not a function.")