import os
import sys
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import mysql.connector


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
        
        if interaction.guild is None:
            await interaction.response.send_message("Sorry, I can't find your server information.")
            return
        
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
        
        rows = mycursor.fetchall()
        
        if rows is None:
            await interaction.response.send_message("No one has been caught yet!")
            return

        res = "```\n"
        res += "{:38s} {:s}\n".format("Username", "Caught Count")
        res += ("-"*51) + "\n"
        for m in rows:
            if m[1] in members:
                res += "{:38s} {:d}\n".format(m[1], int(m[2]))
        res += "```"
        mycursor.close()
        mydb.close()
        await interaction.response.send_message(res)
    
    @nextcord.slash_command(name="fixcaught", description="Fix your username in dad's caught system.")
    async def fixcaught(self, interaction: Interaction, oldname: str):
        """
        [oldname] Fix your username in dad's caught system. Put your old username and descriminator (e.g. DadBot#0001) in the first argument.
        """
        tableName = "caught"
        if interaction.guild is None:
            await interaction.response.send_message("Sorry, I can't find your server information.")
            return
        
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"]
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute(f"SELECT count FROM {tableName} WHERE user = %s", (oldname,))
        
        rows = mycursor.fetchall()
        
        if rows is None:
            await interaction.response.send_message("No record of your old username was found. Please make sure you typed it correctly.")
            return
        
        oldCount = rows[0][0]
        
        mycursor.execute(f"UPDATE {tableName} SET count = count + {oldCount} WHERE user = '{str(interaction.user)}'")
        mycursor.execute(f"UPDATE {tableName} SET user_id = {interaction.user.id} WHERE user = '{str(interaction.user)}'")
        
        mydb.commit()
        mycursor.close()
        mydb.close()
        await interaction.response.send_message("Your username has been updated in Dad's caught system.")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Caught(bot))
