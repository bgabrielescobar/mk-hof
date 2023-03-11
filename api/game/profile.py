import json
from PIL import Image, ImageDraw, ImageFont
from api.game.manager.file_manager import *
import config.settings as setting

class Profile:

  profile_bg = "assets/player/user_profile_"
  path_profile_save = "api/game/db/cache/profile/"
  path_font = "/discord-bot"
  path_font = "C:/Users/Usuario/Documents/git/python/discord-bot/assets/fonts/"
  player = {}
  coord_ui_profile_text = {}

  def get_user_stats(self, user_id):

        users_data = FileManager.get_json(FileManager.USERS_JSON)
          
        self.player = users_data[user_id]
        #To Do mostrar que el usuario exista

        overlay_image = Image.open(f"{self.profile_bg}{self.player['class']}.png")

        draw = ImageDraw.Draw(overlay_image)

        self.generate_ui_text()

        for i in range(len(self.coord_ui_profile_text)):
          font = ImageFont.truetype(self.coord_ui_profile_text[i]['type-font'], size= self.coord_ui_profile_text[i]["font-size"])
          draw.text(
            ( 
              self.coord_ui_profile_text[i]["x"],
              self.coord_ui_profile_text[i]["y"]),
              str(self.coord_ui_profile_text[i]["text"]),
              fill=(self.coord_ui_profile_text[i]["font-color"]),
              font=font,
              align='center'
            )

        overlay_image.save(f"{self.path_profile_save}{user_id}.png", quality=50)
        
        return f"{self.path_profile_save}{user_id}.png"

  def generate_ui_text(self):
     
     experience_remaining = setting.export_settings("exp-level")[self.player['lv'] - 1]
     self.coord_ui_profile_text = [
        {"x": 230, "y": 25, "text": self.player['name'], "font-size": 20, "font-color": (250, 250, 250), "type-font": f"{self.path_font}ANTON.TTF"},
        {"x": 425, "y": 30, "text": self.player['lv'], "font-size": 42, "font-color": (194, 235, 167), "type-font": f"{self.path_font}ANTON.TTF"},
        {"x": 260, "y": 54, "text": f"{self.player['exp']}/{experience_remaining}", "font-size": 14, "font-color": (25, 25, 25), "type-font": f"{self.path_font}ANTON.TTF"},
        {"x": 398, "y": 105, "text": self.player['max-life'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.path_font}ANTON.TTF"},
        {"x": 398, "y": 132, "text": self.player['attack'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.path_font}ANTON.TTF"},
        {"x": 398, "y": 160, "text": self.player['defense'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.path_font}ANTON.TTF"},
        {"x": 398, "y": 206, "text": self.player['gold'], "font-size": 16, "font-color": (250, 250, 250), "type-font": f"{self.path_font}ANTON.TTF"},
     ]
       
    