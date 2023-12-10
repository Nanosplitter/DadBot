import os
from urllib import response
import openai
import yaml
import json
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from noncommands.dadroid import dadroid_single

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

        await interaction.response.defer()

        await dadroid_single(
            "You are a translator. Your goal is to translate the following message to English. Only reply with the translation and nothing else.",
            message.content,
            first_send_method=interaction.followup.send,
            send_method=interaction.followup.send,
            response_starter=f"Translation of: {message.jump_url}\n >>> ",
            beef=True,
        )


def setup(bot):
    bot.add_cog(Translate(bot))
