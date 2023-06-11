import hashlib
import os
import random
import sys
import uuid
import aiofiles
import aiohttp
import nextcord
import requests
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class NewPicture(commands.Cog, name="newpicture"):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="newdog", description="Creates a picture of a dog that does not exist.(From https://random.dog/)")
    async def newdog(self, interaction: Interaction):
        """
        [No Arguments] Gets a random dog pic from https://random.dog
        """
        url = "https://random.dog/woof.json"
        response = requests.get(url)
        json = response.json()
        await interaction.response.send_message(json["url"])  
    
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(NewPicture(bot))
