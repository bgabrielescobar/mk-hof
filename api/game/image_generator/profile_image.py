import config.settings as setting
import io
from api.game.image_generator.file_manager import *
from PIL import Image, ImageDraw, ImageFont
from api.game.image_generator.base.image_base import ImageBase

class ProfileImage(ImageBase):

    images = {}

    #Placeholder img; Player enemy and background
    preset_figther_img = ''

    battle_ui_location = ''

    img_battle_stage = ''
    enemy_desc_ui = []

    coord_ui_profile_text = []

    def __init__(self):

        self.list_img_generated = []

        experience_remaining = setting.export_settings()["exp-level"][self.player['lv'] - 1]

        self.coord_ui_profile_text = [
        {"coodr": (230, 25), "text": self.player['name'], "font-size": 20, "font-color": (250, 250, 250), "type-font": f"{self.ANTON_FONT}"},
        {"coodr": (425, 30), "text": self.player['lv'], "font-size": 42, "font-color": (194, 235, 167), "type-font": f"{self.ANTON_FONT}"},
        {"coodr": (260, 54), "text": f"{self.player['exp']}/{experience_remaining}", "font-size": 14, "font-color": (25, 25, 25), "type-font": f"{self.ANTON_FONT}"},
        {"coodr": (398, 105), "text": self.player['max-life'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.ANTON_FONT}"},
        {"coodr": (398, 132), "text": self.player['attack'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.ANTON_FONT}"},
        {"coodr": (398, 160), "text": self.player['defense'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.ANTON_FONT}"},
        {"coodr": (398, 206), "text": self.player['gold'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.ANTON_FONT}"},
     ]
 

    def player_profile(self):

        profile_image = Image.open(f"{self.PATH_PLAYER_PROFILE}{self.player['class']}{self.PNG_EXT}")
        
        draw = ImageDraw.Draw(profile_image)

        for coord_profile in self.coord_ui_profile_text:
          font = ImageFont.truetype(coord_profile['type-font'], size= coord_profile["font-size"])
          draw.text(coord_profile["coodr"], str(coord_profile["text"]), fill=(coord_profile["font-color"]), font=font)

        return self.convert_img_to_bytes(profile_image)

    def generate_image(self, func_name, *args):
        
        self.total_images += 1

        try:
            function_call = eval('self.' + func_name)
        except NameError:
            print(f"Function '{func_name}' not defined.")
        else:
            if callable(function_call):
                image_path = function_call(*args)
                return image_path
            else:
                print(f"'{func_name}' is not a function.")
        