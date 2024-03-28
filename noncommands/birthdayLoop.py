import datetime
from peewee import fn
from models.birthday import Birthday


class BirthdayLoop:
    def __init__(self, bot):
        self.bot = bot

    async def checkBirthdays(self):
        print("Running Birthday Checker")

        today = datetime.datetime.now()

        query = Birthday.select().where(
            (fn.MONTH(Birthday.birthday) == today.month)
            & (fn.DAY(Birthday.birthday) == today.day)
        )

        for birthday in query:
            for channel in self.bot.get_all_channels():
                if str(birthday.channel_id) == str(channel.id):
                    await channel.send(f"# {birthday.mention}'s birthday is today!")
