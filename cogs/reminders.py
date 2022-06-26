import os
import sys
import yaml
from nextcord.ext import commands
from noncommands import summarizer
import dateparser as dp
import mysql.connector
from dateparser.search import search_dates

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Reminders(commands.Cog, name="reminders"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remindme")
    async def remindme(self, context, *args):
        """
        Has DadBot remind you at a specific time. 
        """
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        timeStr = " ".join(args).lower()
        time = dp.parse(timeStr, settings={'TIMEZONE': 'US/Eastern', 'RETURN_AS_TIMEZONE_AWARE': True, 'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first'})
        timeWords = timeStr
        f = '%Y-%m-%d %H:%M:%S'
        if time is None:
            searchRes = search_dates(timeStr, settings={'TIMEZONE': 'US/Eastern', 'RETURN_AS_TIMEZONE_AWARE': True, 'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first'}, languages=['en'])
            for t in searchRes:
                time = t[1]
                timeWords = t[0]
                break
            
        if time is not None:
            timeUTC = dp.parse(time.strftime(f), settings={'TIMEZONE': 'US/Eastern', 'TO_TIMEZONE': 'UTC'})
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("INSERT INTO reminders (author, message_id, remind_time) VALUES ('"+ str(context.message.author) +"', '"+ str(context.message.id) +"', '"+ timeUTC.strftime(f) +"')")

            await context.reply("You will be reminded at: " + time.strftime(f) + " EST \n\nHere's the time I read: " + timeWords)
            mydb.commit()
            mycursor.close()
            mydb.close()
        else:
            await context.reply("I can't understand that time, try again but differently")

   
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Reminders(bot))
