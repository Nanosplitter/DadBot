import os
import mysql.connector
import dateparser as dp
from dateparser.search import search_dates
import yaml
from nextcord.ext import commands

from noncommands import birthdayLoop

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Birthday(commands.Cog, name="birthday"):
    def __init__(self, bot):
        self.bot = bot
        self.birthdayLoop = birthdayLoop.BirthdayLoop(bot)

    @commands.command(name="setbirthday")
    async def setbirthday(self, context, *birthday):
        """
        Dad always remembers birthdays.
        """
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        timeStr = " ".join(birthday).lower()
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
            mycursor.execute(f"DELETE FROM birthdays WHERE author = '{context.message.author}'")
            mydb.commit()
            mycursor.execute("INSERT INTO birthdays (author, mention, channel_id, birthday) VALUES ('"+ str(context.message.author) +"', '"+ str(context.message.author.mention) +"', '"+ str(context.channel.id) +"', '"+ timeUTC.strftime(f) +"')")
            print(time)
            await context.reply("Your Birthday is set for: " + time.strftime(f) + " EST \n\nHere's the time I read: " + timeWords)
            mydb.commit()
            mycursor.close()
            mydb.close()
        else:
            await context.reply("I can't understand that time, try again but differently")
    
    @commands.command(name="todaysbirthdays")
    async def todaysbirthdays(self, context):
        await self.birthdayLoop.checkBirthdays()

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Birthday(bot))
