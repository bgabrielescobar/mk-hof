import json
import io
import config.settings as setting
from PIL import Image, ImageDraw, ImageFont

class Create:

    welcome_user_game = 'assets/ui/title_game.png'
    select_class = 'assets/ui/create_player.png'

    ANOTHER_ROUND_FONT = "C:/Users/Usuario/Documents/git/python/discord-bot/assets/fonts/ANOTHER_ROUND.OTF"

    def create_user(self, user_id, user_class):
        
        with open('api/game/db/users.json', 'r') as file:
            data = json.load(file)

        config = setting.export_settings("classes")["create"][user_class]

        data[user_id] = {
            "name": f"{user_id}",
            "lv": 1,
            "exp":0,
            "attack": config['attack'],
            "defense": config['defense'],
            "max-life": config['life'],
            "current-life": config['life'],
            "dmg-taken":0,
            "gold": 0,
            "items": {},
            "crit": config['crit'],
            "dodge": config['dodge'],
            "path-img": config['path-img'],
            "class": user_class
        }

        with open('api/game/db/users.json', 'w') as file:
            json.dump(data, file, indent=4)

        wimage_open = Image.open(self.welcome_user_game)

        to_draw_image = ImageDraw.Draw(wimage_open)

        font_anton_26 = ImageFont.truetype(self.ANOTHER_ROUND_FONT, 26)

        to_draw_image.text((100, 150), user_id, font=font_anton_26)

        #image_on_bytes = ImageFilter.convert_img_to_bytes(wimage_open)

        return image_on_bytes

    def get_classes(self, user_id):
        with open('api/game/db/users.json', 'r') as file:
            data = json.load(file)
            
        return self.select_class
