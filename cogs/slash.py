from cgi import test
import os
import sys
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

testingServer = 850473081063211048

# Here we name the cog and create a new class for the cog.
class Slash(commands.Cog, name="slash"):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="zing", description="this zing the server")
    async def zing(self, interaction: Interaction, number: Optional[int] = SlashOption(required=False)):
        await interaction.response.send_message("ZIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIING " * number)
    
    @nextcord.slash_command(name="echo", description="say it back", guild_ids=[testingServer])
    async def ping(self, interaction: Interaction, words: str = SlashOption(required=True)):
        await interaction.response.send_message(words)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Slash(bot))
