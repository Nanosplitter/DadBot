import os
import sys
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import mysql.connector
import time
from services.db_service import *
from models.caught import get_all_in_server, Caught


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Caught(commands.Cog, name="caught"):
    def __init__(self, bot):
        self.bot = bot
        self.old_names = dict()

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @nextcord.slash_command(name="caught", description="See how many times everyone on the server has been caught by DadBot.")
    async def caught(self, interaction: Interaction):
        """
        [No Arguments] See how many times everyone on the server has been caught by DadBot.
        """
        
        if interaction.guild is None:
            await interaction.response.send_message("Sorry, I can't find your server information.")
            return

        embeds = []
        position = 0

        position_colors = {
            0: 0xffd700,
            1: 0xc0c0c0,
            2: 0xcd7f32
        }

        for caught in get_all_in_server(interaction.guild.members):
            member = nextcord.utils.get(interaction.guild.members, id=int(caught.user_id))

            if position < 3:
                embed = nextcord.Embed(title="", color=position_colors[position])
                position += 1
            else:
                embed = nextcord.Embed(title="")

            if member is not None:
                embed = caught.build_embed(member, embed.color)
                embeds.append(embed)

        if len(embeds) == 0:
            await interaction.response.send_message("No one has been caught yet! \nTry running `/fixcaughtids` if you expected stuff to show up here.")
            return

        firstMessage = True

        embed_group = []
        for embed in embeds:
            embed_group.append(embed)
            if len(embed_group) == 9:
                if firstMessage:
                    await interaction.response.send_message(embeds=embed_group)
                    firstMessage = False
                else:
                    await interaction.channel.send(embeds=embed_group)
                embed_group = []

        if len(embed_group) > 0:
            if firstMessage:
                await interaction.response.send_message(embeds=embed_group)
            else:
                await interaction.channel.send(embeds=embed_group)
    
    @nextcord.slash_command(name="fixcaught", description="Fix your username in dad's caught system.")
    async def fixcaught(self, interaction: Interaction, oldname: str):
        """
        [oldname] Fix your username in dad's caught system. Put your old username and descriminator (e.g. DadBot#0001) in the first argument.
        """
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

        mycursor.execute(f"SELECT count FROM {self.table} WHERE user = %s", (oldname,))
        
        rows = mycursor.fetchall()
        
        if rows is None:
            await interaction.response.send_message("No record of your old username was found. Please make sure you typed it correctly.")
            return
        
        oldCount = rows[0][0]

        mycursor.execute(f"SELECT * FROM {self.table} WHERE user = '{interaction.user}'")
        hascolumn = False
        for m in mycursor:
            hascolumn = True
        
        if hascolumn:
            mycursor.execute(f"UPDATE {self.table} SET count = count + {oldCount} WHERE user = '{str(interaction.user)}'")
            mycursor.execute(f"UPDATE {self.table} SET user_id = {interaction.user.id} WHERE user = '{str(interaction.user)}'")
        else:
            mycursor.execute(f"INSERT INTO {self.table} (user_id, user, count) VALUES ('{interaction.user.id}', '{str(interaction.user)}', {oldCount})")
        
        mycursor.execute(f"DELETE FROM {self.table} WHERE user = '{oldname}'")

        self.bot.logger.info(f"User {interaction.user} updated their username from {oldname} to {str(interaction.user)}")
        
        mydb.commit()
        mycursor.close()
        mydb.close()
        await interaction.response.send_message("Your username has been updated in Dad's caught system.")
    
    @fixcaught.on_autocomplete("oldname")
    async def meme_autocomplete(self, interaction: Interaction, search: str):
        """
        [Text] Make a meme with custom text
        """
        
        if "old_names" not in self.old_names.keys() or self.old_names["last_cache"] + 500 < time.time():
            mydb = mysql.connector.connect(
                host=config["dbhost"],
                user=config["dbuser"],
                password=config["dbpassword"],
                database=config["databasename"]
            )
            mycursor = mydb.cursor(buffered=True)

            mycursor.execute(f"SELECT user FROM {self.table} ORDER BY count DESC")

            rows = mycursor.fetchall()

            if rows is None:
                return
            
            self.old_names["old_names"] = []
            
            for m in rows:
                self.old_names["old_names"].append(m[0])
            
            self.old_names["last_cache"] = time.time()
            mycursor.close()
            mydb.close()

        old_names = []
        for name in self.old_names["old_names"]:
            if search.lower() in name.lower() and not name.lower().endswith("#0"):
                old_names.append(name)
            
        await interaction.response.send_autocomplete(old_names[:25])
    
    @nextcord.slash_command(name="fixcaughtids", description="Fix the caught IDs for users in the database")
    async def fixcaughtids(self, interaction: Interaction):
        """
        [No Arguments] Fix the caught IDs for users in the database
        """
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

        mycursor.execute(f"SELECT * FROM {self.table}")
        
        rows = mycursor.fetchall()
        
        if rows is None:
            await interaction.response.send_message("No one has been caught yet!")
            return
        
        for m in rows:
            if m[2].endswith("#0"):
                user = nextcord.utils.get(interaction.guild.members, name=m[2].split("#")[0])
                if user is not None:
                    mycursor.execute(f"UPDATE {self.table} SET user_id = {user.id} WHERE user = '{m[2]}'")
                    self.bot.logger.info(f"Updated {m[2]}'s ID to {user.id}")
        
        mydb.commit()
        mycursor.close()
        mydb.close()
        await interaction.response.send_message("All caught IDs have been updated.")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Caught(bot))
