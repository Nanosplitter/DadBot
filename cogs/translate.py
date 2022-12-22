import os
import openai
import yaml
import json
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from googletrans import Translator
translator = Translator()

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Translate(commands.Cog, name="translate"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.message_command(name="translate")
    async def translate(self, interaction: Interaction, message: nextcord.Message):
        """
        Translate a message to English.
        """
        await interaction.response.send_message(translator.translate(message.content).text)

def setup(bot):
    bot.add_cog(Translate(bot))