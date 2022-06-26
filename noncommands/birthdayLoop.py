import yaml
import sys
import os
import mysql.connector
if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class BirthdayLoop:
    def __init__(self, bot):
        self.bot = bot
    async def checkBirthdays(self):
        print("Running Birthday Checker")
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT author, mention, birthday, channel_id FROM birthdays WHERE DAY(birthday) = DAY(CONVERT_TZ(NOW(), '+00:00', '-05:00')) AND MONTH(birthday) = MONTH(CONVERT_TZ(NOW(), '+00:00', '-05:00'))")
        for m in mycursor:
            for channel in self.bot.get_all_channels():
                if m[3] == str(channel.id):
                    await channel.send(f"{m[1]}'s birthday is today!")


        mydb.commit()
        mycursor.close()
        mydb.close()