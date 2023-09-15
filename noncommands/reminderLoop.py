import yaml
import sys
import os
import mysql.connector
import nextcord
from nextcord.utils import format_dt
import pytz

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
            channel = bot.get_channel(int(m[5]))

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
                embed = nextcord.Embed(title=m[3], color=0x00ff00)
                time = m[4]
                time = time.replace(tzinfo=pytz.utc)

                embed.add_field(name=f"When", value=f'{format_dt(time, "f")} ({format_dt(time, "R")})', inline=False)
                await msg.reply(f"Hey <@{m[2]}>, you asked me to remind you of [this]({msg.jump_url}):", embed=embed)
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