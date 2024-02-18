import os
import sys
import inspect

import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import yaml
from nextcord.ext import commands
from nextcord.ui import Button, View

from noncommands.chatsplit import chat_split

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="help", description="List all of Dad's commands")
    async def help(self, interaction: Interaction):
        await interaction.response.defer()

        commands = self.bot.get_all_application_commands()

        cogs = dict()

        for command in commands:
            if command.parent_cog.qualified_name not in cogs:
                cogs[command.parent_cog.qualified_name] = command.parent_cog

        message = "# DadBot\n\n"

        excluded_cogs = ["moderation", "steps"]

        for cog in cogs:
            if cog in excluded_cogs:
                continue
            message += "## " + cog.capitalize() + "\n\n--------------\n"
            cog_commands = cogs[cog].application_commands
            for command in cog_commands:
                message += build_command_string(command, interaction)
            message += "\n"

        messages = chat_split(message, help=True)

        first_message = True
        for message in messages:
            if first_message:
                await interaction.followup.send(message)
                first_message = False
            else:
                await interaction.channel.send(message)


def build_command_string(command, interaction: Interaction):
    message = ""
    if command.type != 3:
        message += f"- **`/{command.name}`: {command.description}**\n"
    else:
        message += f"- (message options > apps) > **`{command.name}`: {command.callback.__doc__.strip()}**\n"

    payload = command.get_payload(interaction.guild_id)
    if "options" in payload:
        options = payload["options"]
        for option in options:
            message += f"  - **{option['name']}**: {option['description']} ({'required' if 'required' in option else 'optional'})\n"
            if "options" in option:
                for sub_option in option["options"]:
                    message += f"    - **{sub_option['name']}**: {sub_option['description']} ({'required' if 'required' in sub_option else 'optional'})\n"

    return message


def setup(bot):
    bot.add_cog(Help(bot))
