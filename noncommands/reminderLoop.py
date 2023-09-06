import yaml
import sys
import os
import mysql.connector

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

        mycursor.execute("SELECT * FROM remindme WHERE time <= UTC_TIMESTAMP();")

        for m in mycursor:

            print(m)

            channel = bot.get_channel(int(m[5]))
            print

            print(channel)

            if channel is None:
                continue

            if m[6] == "-1":
                await channel.send(f"Hey <@{m[2]}>, you asked me to remind you of this:\n\n{m[3]}")
                continue

            try:
                msg = await channel.fetch_message(m[6])
            except:
                continue
            try:
                await msg.reply(f"Hey <@{m[2]}>, you asked me to remind you of this:\n\n{m[3]}")
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
        
        mycursor.execute("DELETE FROM remindme WHERE time <= UTC_TIMESTAMP();")

        mydb.commit()
        mycursor.close()
        mydb.close()