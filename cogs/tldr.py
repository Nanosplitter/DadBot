import os
import sys
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from noncommands import summarizer

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class TLDR(commands.Cog, name="tldr"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="tldrchannel", description="Get a TLDR of X number of past messages on the channel.")
    async def tldrchannel(self, interaction: Interaction, number: Optional[int] = SlashOption(description="The number of past messages to summarize", required=True, min_value=5, max_value=200)):
        """
        [NumberOfMessages] Get a TLDR of X number of past messages on the channel.
        """

        messages = await interaction.channel.history(limit=number).flatten()
        text = ". ".join([m.content for m in messages])
        text = text.replace(".. ", ". ")
        embed = summarizer.getSummaryText(config, text)

        await interaction.response.send_message(embed=embed)
    
    @nextcord.slash_command(name="tldr", description="Get a TLDR of a web page.")
    async def tldr(self, interaction: Interaction, url: Optional[str] = SlashOption(description="The URL of the web page to summarize", required=True)):
        """
        [URL] Get a TLDR a web page.
        """
        try:
            await interaction.response.send_message(embed=summarizer.getSummaryUrl(config, url))
        except:
            await interaction.response.send_message("There's something odd about that link. Either they won't let me read it or you sent it wrongly.")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(TLDR(bot))