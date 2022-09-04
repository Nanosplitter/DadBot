import os
import sys
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import mysql.connector

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Caught(commands.Cog, name="caught"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @nextcord.slash_command(name="caught", description="See how many times everyone on the server has been caught by DadBot.")
    async def caught(self, interaction: Interaction):
        """
        [No Arguments] See how many times everyone on the server has been caught by DadBot.
        """
        members = []
        for i in interaction.guild.members:
            members.append(str(i))
        
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"]
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT * FROM caught ORDER BY count DESC")

        res = "```\n"
        res += "{:38s} {:s}\n".format("Username", "Caught Count")
        res += ("-"*51) + "\n"
        for m in mycursor:
            if m[1] in members:
                res += "{:38s} {:d}\n".format(m[1], int(m[2]))
        res += "```"
        mycursor.close()
        mydb.close()
        await interaction.response.send_message(res)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Caught(bot))
