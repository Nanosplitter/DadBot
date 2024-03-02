import os
import mysql.connector
import dateparser as dp
from dateparser.search import search_dates
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord.ui import Button, View, TextInput
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel

from services.step_log_service import (
    build_embed_for_server,
    submit_step_log,
    build_step_logger_button,
)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Steps(commands.Cog, name="steps"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="steps", description="Get the current steps leaderboard."
    )
    async def steps(self, interaction: Interaction):

        step_embed = build_embed_for_server(interaction.guild)

        step_logger_button = build_step_logger_button()

        view = View(timeout=None)
        view.add_item(step_logger_button)

        await interaction.response.send_message(embed=step_embed, view=view)

    @nextcord.slash_command(name="logsteps", description="Log your steps for the day.")
    async def logsteps(
        self,
        interaction: Interaction,
        steps: Optional[int] = SlashOption(
            description="Your total steps for the day", required=True
        ),
    ):
        submit_step_log(interaction.guild.id, interaction.user.id, steps)

        await interaction.response.send_message(
            f"{interaction.user.mention} logged {steps} steps!"
        )


def setup(bot):
    bot.add_cog(Steps(bot))
