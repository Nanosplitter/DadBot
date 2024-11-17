import os
from urllib import response
import openai
import yaml
import json
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from noncommands.dadroid import dadroid_multiple
from noncommands.chat import Chat

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Translate(commands.Cog, name="translate"):
    def __init__(self, bot):
        self.bot = bot

    async def handle_translation(self, interaction: Interaction, message: nextcord.Message, translation_type: str, response_starter: str):
        await interaction.response.defer()
        chat = Chat(self.bot)
        prepared_messages = await chat.prepare_chat_messages([message])
        await dadroid_multiple(
            f"You are a translator. Your goal is to translate the following message to {translation_type}. Only reply with the translation and nothing else. If the message is an image, translate the text in the image to {translation_type}.",
            prepared_messages[0],
            first_send_method=interaction.followup.send,
            send_method=interaction.followup.send,
            response_starter=response_starter,
            beef=True,
        )

    @nextcord.message_command(name="translate")
    async def translate(self, interaction: Interaction, message: nextcord.Message):
        """
        Translate a message to English.
        """
        await self.handle_translation(
            interaction,
            message,
            "English",
            f"Translation of: {message.jump_url}\n >>> "
        )

    @nextcord.message_command(name="zoomer")
    async def zoomer(self, interaction: Interaction, message: nextcord.Message):
        """
        Translate a message to Zoomer.
        """
        await self.handle_translation(
            interaction,
            message,
            "Gen-Z-speak",
            f"Zoomer Translation of: {message.jump_url}\n >>> "
        )

    @nextcord.message_command(name="boomer")
    async def boomer(self, interaction: Interaction, message: nextcord.Message):
        """
        Translate a message to Boomer.
        """
        await self.handle_translation(
            interaction,
            message,
            "Boomer-speak",
            f"Boomer Translation of: {message.jump_url}\n >>> "
        )


def setup(bot):
    bot.add_cog(Translate(bot))
