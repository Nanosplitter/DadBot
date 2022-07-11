import os
import sys
import yaml
from nextcord.ext import commands
import mysql.connector

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Settings(commands.Cog, name="settings"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setcaughtchance")
    async def setcaughtchance(self, context, param):
        """
        Set the % chance of getting caught by dad bot for an "I'm"
        """

        try:
            percent = int(param)
            if percent < 0 or 100 < percent:
                context.reply("Your percentage has to be in the 0-100 range")
                return
        except:
            context.reply("I can't understand that percentage. You need to do a number between 0 and 100 inclusive")

        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"]
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT * FROM server_settings WHERE server_id = '" + str(context.message.guild.id) + "'")

        hascolumn = False
        for m in mycursor:
            hascolumn = True

        if not hascolumn:
            mycursor.execute("INSERT INTO server_settings (server_id) VALUES ('"+ str(context.message.guild.id) +"')")
        else:
            mycursor.execute("UPDATE caught SET count = count + 1 WHERE user = '" + str(context.message.author) + "'")

        mydb.commit()
        mycursor.close()
        mydb.close()
    

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Settings(bot))