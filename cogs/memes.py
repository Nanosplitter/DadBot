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
    
    @nextcord.slash_command(name="emojitype", description="Make a message with letter emojis")
    async def nobitches(self, interaction: Interaction, text: str = SlashOption(description="Message to send", required=True)):
        """
        [Text] Make a message with letter emojis
        """
        emoji_mappings = {
            "a": ":regional_indicator_a:",
            "b": ":regional_indicator_b:",
            "c": ":regional_indicator_c:",
            "d": ":regional_indicator_d:",
            "e": ":regional_indicator_e:",
            "f": ":regional_indicator_f:",
            "g": ":regional_indicator_g:",
            "h": ":regional_indicator_h:",
            "i": ":regional_indicator_i:",
            "j": ":regional_indicator_j:",
            "k": ":regional_indicator_k:",
            "l": ":regional_indicator_l:",
            "m": ":regional_indicator_m:",
            "n": ":regional_indicator_n:",
            "o": ":regional_indicator_o:",
            "p": ":regional_indicator_p:",
            "q": ":regional_indicator_q:",
            "r": ":regional_indicator_r:",
            "s": ":regional_indicator_s:",
            "t": ":regional_indicator_t:",
            "u": ":regional_indicator_u:",
            "v": ":regional_indicator_v:",
            "w": ":regional_indicator_w:",
            "x": ":regional_indicator_x:",
            "y": ":regional_indicator_y:",
            "z": ":regional_indicator_z:",
            " ": "   ",
            "0": ":regional_indicator_zero:",
            "1": ":regional_indicator_one:",
            "2": ":regional_indicator_two:",
            "3": ":regional_indicator_three:",
            "4": ":regional_indicator_four:",
            "5": ":regional_indicator_five:",
            "6": ":regional_indicator_six:",
            "7": ":regional_indicator_seven:",
            "8": ":regional_indicator_eight:",
            "9": ":regional_indicator_nine:",
            "!": ":grey_exclamation:",
            "?": ":grey_question:",
            "#": ":hash:",
            "*": ":asterisk:"
        }

        res = [f"{emoji_mappings[letter]}" if letter in emoji_mappings else letter for letter in text.lower()]

        await interaction.response.send_message("".join(res))
                
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Memes(bot))
