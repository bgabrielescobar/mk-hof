import imageio
import abc
import io
import pygifsicle
from PIL import Image

class ImageBase(metaclass=abc.ABCMeta):

    # Counter images generated to create gif
    total_images = -1

    # Coordenates to render player and enemy on battle stage
    fighters_positions = [
            {"x":300, "y": 50}, # Enemy
            {"x":60, "y": 50},  # Player
    ]

    battle_ui_color = {
        "red_color": (255, 95, 95),
        "black":     (0, 0, 0)
    }

    PATH_BATTLE_BACKGROUND = "assets/ui/battle_background_"

    PNG_EXT = '.png'

    path_img_db_cache = {
        "farm": "api/game/db/cache/farm/"
    }

    list_img_generated = []

    PATH_LOSE_SCREEN = 'assets/ui/lose_screen.png'
    PATH_WIN_SCREEN = 'assets/ui/victory_screen.png'
    PATH_DRAW_SCREEN = 'assets/ui/draw_screen.png'
    PATH_LVL_UP_SCREEN = 'assets/player/lvl_up.png'
    PATH_PLAYER_PROFILE = "assets/player/user_profile_"
    
    ANTON_FONT = "C:/Users/Usuario/Documents/git/python/discord-bot/assets/fonts/ANTON.TTF"
    ANOTHER_ROUND_FONT = "C:/Users/Usuario/Documents/git/python/discord-bot/assets/fonts/ANOTHER_ROUND.OTF"

    player = {}
    enemy = {}

    def generate_resume_battle_gif(self):
        
        gif_bytes = io.BytesIO()

        imageio.mimsave(gif_bytes, self.list_img_generated, format='GIF', duration=1)

        with open('api/game/db/cache/farm/animated.gif', 'wb') as f:
            f.write(gif_bytes.getvalue())
            
        gif_bytes.close()

        pygifsicle.optimize('api/game/db/cache/farm/animated.gif')
        
        return 'api/game/db/cache/farm/animated.gif'

    def convert_img_to_bytes(self, image):

        buffer = io.BytesIO()
        
        image.save(buffer, format='png')

        bytes_imagen = buffer.getvalue()

        buffer.close()

        return io.BytesIO(bytes_imagen)

    @abc.abstractmethod
    def generate_image(self):
         pass