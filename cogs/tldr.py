import os
import sys
import yaml
from nextcord.ext import commands
from noncommands import summarizer

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class TLDR(commands.Cog, name="tldr"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tldrchannel")
    async def tldrchannel(self, context, param):
        """
        [NumberOfMessages] Get a TLDR of X number of past messages on the channel.
        """
        if param.isnumeric() and int(param) >= 5:
            messages = await context.channel.history(limit=int(param)).flatten()
            text = ". ".join([m.content for m in messages])
            text = text.replace(".. ", ". ")
            embed = summarizer.getSummaryText(config, text)
        else:
            await context.reply(f'That number is either not a number or is less than 5. Try `{config["bot_prefix"]}tldrchannel 5` or higher')
            return

        await context.send(embed=embed)
    
    @commands.command(name="tldr")
    async def tldr(self, context, url):
        """
        [URL] Get the invite link of the bot to be able to invite it to another server.
        """
        try:
            await context.send(embed=summarizer.getSummaryUrl(config, url))
        except:
             await context.send("There's something odd about that link. Either they won't let me read it or you sent it wrongly.")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(TLDR(bot))