import os
import mysql.connector
import dateparser as dp
from dateparser.search import search_dates
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel


from noncommands import birthdayLoop


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


# Here we name the cog and create a new class for the cog.
class Birthday(commands.Cog, name="birthday"):
    def __init__(self, bot):
        self.bot = bot
        self.birthdayLoop = birthdayLoop.BirthdayLoop(bot)

    @nextcord.slash_command(
        name="setbirthday", description="Dad always remembers birthdays."
    )
    async def setbirthday(
        self,
        interaction: Interaction,
        birthday: str = SlashOption(
            description="A date, like 'January 4th'", required=True
        ),
    ):
        """
        [Date] Dad always remembers birthdays.
        """
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True,
        )
        timeStr = birthday
        time = dp.parse(
            timeStr,
            settings={
                "TIMEZONE": "US/Eastern",
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "PREFER_DAY_OF_MONTH": "first",
            },
        )
        timeWords = timeStr
        f = "%Y-%m-%d %H:%M:%S"
        if time is None:
            searchRes = search_dates(
                timeStr,
                settings={
                    "TIMEZONE": "US/Eastern",
                    "RETURN_AS_TIMEZONE_AWARE": True,
                    "PREFER_DATES_FROM": "future",
                    "PREFER_DAY_OF_MONTH": "first",
                },
                languages=["en"],
            )
            for t in searchRes:
                time = t[1]
                timeWords = t[0]
                break

        if time is not None:
            timeUTC = dp.parse(
                time.strftime(f),
                settings={"TIMEZONE": "US/Eastern", "TO_TIMEZONE": "UTC"},
            )
            mycursor = mydb.cursor(buffered=True)

            if timeUTC is None:
                await interaction.response.send_message(
                    "Sorry, I can't understand that time, try again but differently"
                )
                return

            if interaction.user is None:
                await interaction.response.send_message(
                    "Sorry, I can't find your user information."
                )
                return

            if interaction.channel is None:
                await interaction.response.send_message(
                    "Sorry, I can't find your channel information."
                )
                return

            mycursor.execute(
                f"DELETE FROM birthdays WHERE author = '{interaction.user.name}' AND channel_id = {interaction.channel.id}"
            )
            mydb.commit()

            mycursor.execute(
                "INSERT INTO birthdays (author, mention, channel_id, birthday) VALUES ('"
                + str(interaction.user.name)
                + "', '"
                + str(interaction.user.mention)
                + "', '"
                + str(interaction.channel.id)
                + "', '"
                + timeUTC.strftime(f)
                + "')"
            )
            await interaction.response.send_message(
                "Your Birthday is set for: "
                + time.strftime(f)
                + " EST \n\nHere's the time I read: "
                + timeWords
            )
            mydb.commit()
            mycursor.close()
            mydb.close()
        else:
            await interaction.response.send_message(
                "I can't understand that time, try again but differently"
            )

    @nextcord.slash_command(
        name="todaysbirthdays", description="Get all of the birthdays for today"
    )
    async def todaysbirthdays(self, interaction: Interaction):
        """
        [No Arguments] Dad will tell you who has birthdays today.
        """
        await interaction.response.send_message("Checking!")
        await self.birthdayLoop.checkBirthdays()


def setup(bot):
    bot.add_cog(Birthday(bot))
