import os
import sys

import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import yaml
from nextcord.ext import commands
from nextcord.ui import Button, View

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    def generateEmbedForCog(self, cog, prefix, index, max_index):
        """
        Generate an embed for a cog.
        """ 
        commands = cog.get_commands()
        command_list = [command.name for command in commands]
        command_description = [command.help for command in commands]

        embed = nextcord.Embed(title="Help: " + cog.qualified_name, description="List of available commands:", color=config["success"])
        for command, description in zip(command_list, command_description):
            embed.add_field(name=prefix + command, value=description)
        
        embed.set_footer(text=f"{index+1}/{max_index}")
        return embed

    @nextcord.slash_command(name="help", description="List all commands from every Cog the bot has loaded.")
    async def help(self, interaction: Interaction):
        """
        How do I find out what all the commands are?
        """

        await interaction.response.send_message("This bot uses slash commands! Type a `/` into the chat, click my icon, and you should see all the commands I can take!")


def setup(bot):
    bot.add_cog(Help(bot))
