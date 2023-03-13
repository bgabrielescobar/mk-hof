from api.game.image_generator.profile_image import *

class Profile(ProfileImage):

  def __init__(self, player):
    self.player = player
    super().__init__()

  def get_user_stats(self):
          
    return self.generate_image('player_profile')
    