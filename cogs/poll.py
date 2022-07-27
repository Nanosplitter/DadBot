import os
import sys
import nextcord
import yaml
from nextcord.ext import commands

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Poll(commands.Cog, name="poll"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        [Question] Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = nextcord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=config["success"]
        )

        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Poll(bot))
