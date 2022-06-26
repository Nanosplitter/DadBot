import yaml
import sys
import os
import mysql.connector
if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class ReminderLoop:

    async def checkReminders(self, bot):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT * FROM reminders WHERE remind_time <= UTC_TIMESTAMP();")

        for m in mycursor:
            for channel in bot.get_all_channels():
                try:
                    msg = await channel.fetch_message(m[2])
                except:
                    continue
                try:
                    await msg.reply("Reminded.")
                    break
                except:
                    pass

        mydb.commit()
        mycursor.close()
        mydb.close()

    async def deleteOldReminders(self, bot):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)
        
        mycursor.execute("DELETE FROM reminders WHERE remind_time <= UTC_TIMESTAMP();")

        mydb.commit()
        mycursor.close()
        mydb.close()