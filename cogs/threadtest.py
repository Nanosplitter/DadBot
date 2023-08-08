import os
import sys
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, Thread, MessageType
from nextcord.abc import GuildChannel


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class ThreadTest(commands.Cog, name="threadtest"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="threadtest", description="This command is used to test thread content")
    async def testcommand(self, interaction: Interaction):
        if not isinstance(interaction.channel, Thread):
            return
        
        thread = interaction.channel
        
        messages = await thread.history(limit=20, oldest_first=True).flatten()

        for message in messages:
            print(f"Message Content:|{message.content}|")
            print(f"Message System Content:|{message.system_content}|")
            print(f"Message Type:{message.type}")
            print("--------------------------")
        
        await interaction.response.send_message("Done!")

def setup(bot):
    bot.add_cog(ThreadTest(bot))
