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
    build_step_logger_view,
    get_steps_logged_graph,
    get_all_user_ids,
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

        await interaction.response.send_message(
            embed=build_embed_for_server(interaction.guild),
            view=build_step_logger_view(),
        )

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

    @nextcord.slash_command(
        name="stepgraph",
        description="Graph things about the step competition",
        guild_ids=[850473081063211048],
    )
    async def graph(self, interaction: Interaction):
        pass

    @graph.subcommand(description="Get a graph of your steps.")
    async def user(self, interaction: Interaction):
        graph = get_steps_logged_graph(interaction.guild, [interaction.user.id])
        await interaction.response.send_message(
            file=nextcord.File(graph),
        )

    @graph.subcommand(description="Get a graph of the server's steps.")
    async def server(self, interaction: Interaction):
        await interaction.response.defer()
        graph = get_steps_logged_graph(
            interaction.guild, get_all_user_ids(interaction.guild.id)
        )
        await interaction.followup.send(
            file=nextcord.File(graph),
        )


def setup(bot):
    bot.add_cog(Steps(bot))
