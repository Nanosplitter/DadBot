import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed
from nextcord.utils import format_dt
import dateparser as dp
from pytz import timezone
from datetime import datetime
import yaml


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Reminders(commands.Cog, name="reminders"):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="remindme", description="Has DadBot remind you of something at a specific time.")
    async def remindme(self, interaction: Interaction, what: str, when: str, tz: str = SlashOption(description="The timezone you want to be reminded in", default="EST", required=False)):
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

        tz = timezone(tz)
        when = dp.parse(when, settings={'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first'})
        when_local = when.astimezone(tz)
        local_utc = when_local.astimezone(timezone("UTC"))

        embed = nextcord.Embed(title=f"New Reminder Created!", color=0x00ff00)

        embed.add_field(name=f"What", value=f"{what}", inline=False)
        embed.add_field(name=f"When", value=f'{format_dt(local_utc, "f")} ({format_dt(local_utc, "R")})', inline=False)
        
        partialMessage = await interaction.response.send_message(embed=embed)

        fullMessage = await partialMessage.fetch()

        f = '%Y-%m-%d %H:%M:%S'

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("INSERT INTO remindme (who, who_id, what, time, channel, message_id) VALUES (%s, %s, %s, %s, %s, %s)", (interaction.user.name, interaction.user.id, what, local_utc.strftime(f), interaction.channel.id, fullMessage.id))

        mydb.commit()
        mycursor.close()
        mydb.close()
        

        

def setup(bot):
    bot.add_cog(Reminders(bot))
