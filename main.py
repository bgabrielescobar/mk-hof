import os
import time
import io
from api.command_manager import CommandManager
#from api.game.manager.file_manager import *
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

channel_shop = 1066866946403999835 # test 1

# @client.event
# async def on_presence_update(before, after):

#     if before.status != after.status:

#         channel = client.get_channel(1073476897972957246)

#         #users = FileManager.get_json(FileManager.USERS_JSON)

#         total_users = users.keys()

#         await channel.edit(name=f"👤{len(total_users)}")

@client.event
async def on_message(message):

  #inicio = time.time()
  
  if message.author.bot:
    return

  if message.content.startswith("!"):

    emoji_list = {
      'shop': ['🟥', '🟦', '🟩', '🤍'],
      'create': ['⚔','🏹','🧙‍♂️']
    }

    [image_bytes, command, file_name] = CommandManager().command_selector(message)
    
    if command in emoji_list.keys():

      message = await client.get_channel(channel_shop).send(file=discord.File(image_bytes))
      
      for emoji in emoji_list[command]:
        await message.add_reaction(emoji)

    elif image_bytes != "":
      
      await message.channel.send(message.author.mention, file=discord.File(image_bytes, file_name))

  #fin = time.time()
  #print(fin-inicio)

@client.event
async def on_reaction_add(reaction, user):
    
    if reaction.message.channel.id == channel_shop and user != client.user:
    
      emoji_list = {
        '🟥': ["create_rune", "attack"],
        '🟦': ["create_rune", "defense"],
        '🟩': ["create_rune", "life"],
        '🤍': ["create_rune", "revive"],
        '⚔': ["create_class", "warrior"],
        '🏹': ["create_class", "ranger"],
        '🧙‍♂️': ["create_class", "mage"],
      }
      
      str_reaction_emoji = str(reaction.emoji)

      if str_reaction_emoji in emoji_list.keys():
        img_generated = CommandManager.emoji_selector(emoji_list[str_reaction_emoji], str(user))
        await user.send(file=discord.File(io.BytesIO(img_generated), 'imagen.png'))

client.run('MTA2NjY4ODQ5MDY0Mjg3MDMyMg.GFMSjR.4aASwsuWOOy3dZuFjcPcAxLi5gILxIiHiCp3Vk')
