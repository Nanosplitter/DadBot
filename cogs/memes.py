import os
import random
import requests
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType, Message
from nextcord.abc import GuildChannel
import uwuify
import json

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Memes(commands.Cog, name="memes"):
    def __init__(self, bot):
        self.bot = bot
        with open("./resources/emoji-mappings.json", encoding="utf8") as file:
            self.emoji_mappings = json.load(file)

    @nextcord.slash_command(name="nobitches", description="Make a No Bitches? Megamind meme with custom text")
    async def nobitches(self, interaction: Interaction, text: str = SlashOption(description="Text to put on the meme", required=True)):
        """
        [Text] Make a No Bitches? Megamind meme with custom text
        """
        params = {
            "template_id": "370867422", 
            "username": "nanosplitter", 
            "password": config["imgflip_pass"],
            "text0": text,
        }
        r = requests.post("https://api.imgflip.com/caption_image", params=params)
        await interaction.response.send_message(r.json()["data"]["url"])

    @nextcord.message_command(name="uwu")
    async def uwu(self, interaction: Interaction, message: nextcord.Message):
        """
        UwU - Wepwy to a message to make it into an UwU message. ( ͡o ꒳ ͡o )
        """
        flags = uwuify.SMILEY | uwuify.YU
        await interaction.response.send_message(uwuify.uwu(message.content, flags=flags))
    
    @nextcord.message_command(name="pastafy")
    async def pastafy(self, interaction: Interaction, message: nextcord.Message):
        """
        [No Arguments] Turns any message you reply to into a copypasta.
        """
        
        res = ""
        for word in message.content.split(" "):
            res += word + (" " + random.choice(self.emoji_mappings[word.lower()]) + " " if word in self.emoji_mappings else " ")
        await interaction.response.send_message(res)
        

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Memes(bot))
