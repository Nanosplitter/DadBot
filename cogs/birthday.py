import datetime
import dateparser as dp
from dateparser.search import search_dates
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel

from noncommands import birthdayLoop
from models.birthday import Birthday

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class BirthdayCog(commands.Cog, name="birthday"):
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
        timeStr = birthday
        timeWords = birthday
        time = dp.parse(
            timeStr,
            settings={
                "TIMEZONE": "US/Eastern",
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "PREFER_DAY_OF_MONTH": "first",
            },
        )

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
            if searchRes:
                time, timeWords = searchRes[0]

        if time:
            timeUTC = dp.parse(
                time.strftime("%Y-%m-%d %H:%M:%S"),
                settings={"TIMEZONE": "US/Eastern", "TO_TIMEZONE": "UTC"},
            )

            if timeUTC is None:
                await interaction.response.send_message(
                    "Sorry, I can't understand that time, try again but differently"
                )
                return

            Birthday.delete().where(
                (Birthday.author == interaction.user.name)
                & (Birthday.channel_id == str(interaction.channel.id))
            ).execute()

            Birthday.create(
                author=interaction.user.name,
                mention=interaction.user.mention,
                channel_id=str(interaction.channel.id),
                birthday=timeUTC,
            )

            await interaction.response.send_message(
                f"Your Birthday is set for: {time.strftime('%Y-%m-%d %H:%M:%S')} EST \n\nHere's the time I read: {timeWords}"
            )

        else:
            await interaction.response.send_message(
                "I can't understand that time, try again but differently"
            )

    @nextcord.slash_command(
        name="todaysbirthdays", description="Get all of the birthdays for today"
    )
    async def todaysbirthdays(self, interaction: Interaction):
        await interaction.response.defer()

        today = datetime.date.today()

        birthdays_today = Birthday.select().where(
            Birthday.birthday.day == today.day, Birthday.birthday.month == today.month
        )

        if not birthdays_today:
            await interaction.followup.send("No birthdays found for today.")
            return

        for birthday in birthdays_today:
            member = await interaction.guild.fetch_member(
                int(birthday.mention.strip("<@!>"))
            )

            if member:
                embed = birthday.build_embed(member, nextcord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                pass


def setup(bot):
    bot.add_cog(BirthdayCog(bot))
