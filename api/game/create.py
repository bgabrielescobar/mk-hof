import json
import config.settings as setting
from PIL import Image, ImageDraw, ImageFont

class Create:

    welcome_user_game = 'assets/ui/title_game.png'
    select_class = 'assets/ui/create_player.png'

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

        to_draw_image = Image.draw(wimage_open)



        return self.welcome_user_game

    def get_classes(self, user_id):
        with open('api/game/db/users.json', 'r') as file:
            data = json.load(file)

        #if data != {} and user_id in data:
        #    return "Ya estas dentro del juego utiliza !info para revisar estadisticas."
            
        return self.select_class
