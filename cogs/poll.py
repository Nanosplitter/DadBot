import os
import sys
import nextcord
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Poll(commands.Cog, name="poll"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="poll", description="Create a poll where members can vote.")
    async def poll(self, interaction: Interaction, question: str = SlashOption(description="Question to ask members.", required=True)):
        """
        [Question] Create a poll where members can vote.
        """
        embed = nextcord.Embed(
            title="A new poll has been created!",
            description=f"{question}",
            color=config["success"]
        )

        embed.set_footer(
            text=f"Poll created by: {interaction.user} • React to vote!"
        )
        
        embed_message = await interaction.response.send_message(embed=embed)
        embed_message = await embed_message.fetch()
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Poll(bot))
