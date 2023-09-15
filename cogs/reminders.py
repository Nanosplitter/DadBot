import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed
from nextcord.utils import format_dt
import dateparser as dp
from pytz import timezone
import pytz
from datetime import datetime
import yaml


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Reminders(commands.Cog, name="reminders"):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="remindme", description="Has DadBot remind you of something at a specific time.")
    async def remindme(self, interaction: Interaction, what: str, when: str, tz: str = SlashOption(description="The timezone you want to be reminded in", default="EDT", required=False)):
        """
        [TextWithDateAndTime] Has DadBot remind you at a specific time.
        """

        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        when_dt = dp.parse(when, settings={'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first', 'TIMEZONE': tz, 'RETURN_AS_TIMEZONE_AWARE': True})
        local_utc = when_dt.astimezone(timezone("UTC"))

        embed = nextcord.Embed(title=f":hammer: New Reminder Created! :hammer:", color=0x00ff00)

        embed.add_field(name=f"What", value=f"{what}", inline=False)
        embed.add_field(name=f"When", value=f'{format_dt(local_utc, "f")} ({format_dt(local_utc, "R")})', inline=False)
        
        partialMessage = await interaction.response.send_message(embed=embed)

        fullMessage = await partialMessage.fetch()

        f = '%Y-%m-%d %H:%M:%S'

        mycursor = mydb.cursor(buffered=True)
        
        mycursor.execute("INSERT INTO remindme (who, who_id, what, time, channel, message_id) VALUES (%s, %s, %s, %s, %s, %s)", (interaction.user.name, interaction.user.id, what, local_utc.strftime(f), interaction.channel.id, fullMessage.id))

        rowId = mycursor.lastrowid

        embed.set_footer(text=f"Run /deletereminder {rowId} to delete this reminder.")

        await fullMessage.edit(embed=embed)

        mydb.commit()
        mycursor.close()
        mydb.close()
    
    @nextcord.slash_command(name="reminders", description="View your reminders.")
    async def reminders(self, interaction: Interaction):
        """
        View your reminders.
        """
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM remindme WHERE who_id = %s ORDER BY time", (interaction.user.id,))

        myresult = mycursor.fetchall()

        if len(myresult) == 0:
            await interaction.response.send_message("You have no reminders!")
            return
    
        embeds = []
        for x in myresult:
            embed = nextcord.Embed(title=f"{x[3]}")

            time = x[4]
            time = time.replace(tzinfo=pytz.utc)

            embed.add_field(name=f"", value=f'{format_dt(time, "f")} ({format_dt(time, "R")})', inline=False)

            embed.set_footer(text=f"Run /deletereminder {x[0]} to delete this reminder.")

            embeds.append(embed)

        await interaction.response.send_message(embeds=embeds)

        mycursor.close()
        mydb.close()
    
    @nextcord.slash_command(name="deletereminder", description="Delete a reminder.")
    async def deletereminder(self, interaction: Interaction, reminder_id: str):
        """
        [ReminderID] Delete a reminder.
        """
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM remindme WHERE who_id = %s AND id = %s", (interaction.user.id, reminder_id))

        res = mycursor.fetchall()

        if len(res) == 0:
            embed = nextcord.Embed(title=f"You have no reminders with that ID!", color=0x00ff00)

            await interaction.response.send_message(embed=embed)
            return

        embed = nextcord.Embed(title=f":x: Deleted Reminder :x:", color=0xff0000)

        time = res[0][4]
        time = time.replace(tzinfo=pytz.utc)

        embed.add_field(name=f"What", value=f"{res[0][3]}", inline=False)
        embed.add_field(name=f"When", value=f'{format_dt(time, "f")} ({format_dt(time, "R")})', inline=False)

        await interaction.response.send_message(embed=embed)

        mycursor.execute("DELETE FROM remindme WHERE who_id = %s AND id = %s", (interaction.user.id, reminder_id))

        mydb.commit()
        mycursor.close()
        mydb.close()
    
    @nextcord.slash_command(name="timetester", description="Test a time string to see what time the bot will think you said.")
    async def timetester(self, interaction: Interaction, when: str, tz: str = SlashOption(description="The timezone you want to be reminded in", default="EDT", required=False)):
        """
        [TextWithDateAndTime] Test a time string to see what time the bot will think you said.
        """
        when_dt = dp.parse(when, settings={'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first', 'TIMEZONE': tz, 'RETURN_AS_TIMEZONE_AWARE': True})
        local_utc = when_dt.astimezone(timezone("UTC"))

        embed = nextcord.Embed(title=f"Time Tester", color=0x00ff00)

        embed.add_field(name=f"Input", value=f"{when}", inline=False)
        embed.add_field(name=f"Input timezone", value=f"{tz}", inline=False)
        embed.add_field(name=f"Input as datetime", value=f"{when_dt}", inline=False)
        embed.add_field(name=f"Input to utc time", value=f"{local_utc}", inline=False)
        embed.add_field(name=f"Input to utc discord time", value=f'`{format_dt(local_utc, "f")} ({format_dt(local_utc, "R")})`', inline=False)
        embed.add_field(name=f"Output from datetime", value=f'{format_dt(when_dt, "f")} ({format_dt(when_dt, "R")})', inline=False)
        embed.add_field(name=f"Output from UTC", value=f'{format_dt(local_utc, "f")} ({format_dt(local_utc, "R")})', inline=False)
        
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Reminders(bot))
