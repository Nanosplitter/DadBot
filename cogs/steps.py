import os
import mysql.connector
import dateparser as dp
from dateparser.search import search_dates
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel


from noncommands import birthdayLoop


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Steps(commands.Cog, name="steps"):
    def __init__(self, bot):
        self.bot = bot

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Steps(bot))
