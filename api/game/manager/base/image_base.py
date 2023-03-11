import imageio
import os
import abc

class ImageBase(metaclass=abc.ABCMeta):

    # Counter images generated to generated gif
    total_images = -1

    path_img_db_cache = {
        "farm": "api/game/db/cache/farm/"
    }

    ANTON_FONT = "C:/Users/Usuario/Documents/git/python/discord-bot/assets/fonts/ANTON.TTF"
    ANOTHER_ROUND_FONT = "C:/Users/Usuario/Documents/git/python/discord-bot/assets/fonts/ANOTHER_ROUND.OTF"

    def generate_resume_battle_gif(self, user_id): 
      
        images = []
        
        for count in range(self.total_images + 1):
            img_path_generated = f"{self.path_img_db_cache['farm']}{user_id}-{count}.png"
            images.append(imageio.imread(img_path_generated))

        gif_path = f"{self.path_img_db_cache['farm']}{user_id}.gif"
        
        # Lista de duracion
        # duration = [1] * 2 + [2] * 5
        
        imageio.mimsave(gif_path, images, 'GIF', duration=1)

        return gif_path
    
    @abc.abstractmethod
    def generate_image(self):
        pass