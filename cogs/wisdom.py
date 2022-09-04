import os
import sys
import aiohttp
import nextcord
import requests
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import inspirobot

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Wisdom(commands.Cog, name="wisdom"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="randomfact", description="Dad has learned a few things, he'll share.")
    async def randomfact(self, interaction: Interaction):
        """
        [No Arguments] Dad has learned a few things, he'll share.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://nextcordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = nextcord.Embed(description=data["text"], color=config["main_color"])
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = nextcord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=config["error"]
                    )
                    await interaction.response.send_message(embed=embed)
    
    @nextcord.slash_command(name="inspire", description="Get an inspirational poster courtesy of https://inspirobot.me/")
    async def inspire(self, interaction: Interaction):
        """
        [No Arguments] Get an inspirational poster courtesy of https://inspirobot.me/
        """
        quote = inspirobot.generate()
        await interaction.response.send_message(quote.url)
    
    @nextcord.slash_command(name="wisdom", description="Get some wisdom courtesy of https://inspirobot.me/")
    async def wisdom(self, interaction: Interaction):
        """
        [No Arguments] Get some wisdom courtesy of https://inspirobot.me/
        """
        flow = inspirobot.flow()  # Generate a flow object
        res = ""
        for quote in flow:
            res += quote.text + "\n"
        
        await interaction.response.send_message(res)

    @nextcord.slash_command(name="advice", description="Get some fatherly advice.")
    async def advice(self, interaction: Interaction):
        """
        [No Arguments] Get some fatherly advice.
        """
        r = requests.get("https://api.adviceslip.com/advice")
        await interaction.response.send_message(r.json()['slip']['advice'])

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Wisdom(bot))
