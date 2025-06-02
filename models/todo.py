from peewee import *
from services.db_service import get_db
import nextcord
from nextcord.utils import format_dt
import pytz
from datetime import datetime as dt


class Todo(Model):
    id = AutoField()
    who = CharField()
    who_id = CharField()
    what = CharField()
    time = DateTimeField()
    channel = CharField()
    message_id = CharField()
    reminded = IntegerField()

    class Meta:
        database = get_db()

    def __repr__(self) -> str:
        return f"{self.who}'s todo item: {self.what} at {self.time}"

    def __str__(self) -> str:
        return f"{self.who}'s todo item: {self.what} at {self.time}"

    def build_embed(self):
        embed = nextcord.Embed(title=self.what)

        if self.time is not None:
            utc_time = self.time.replace(tzinfo=pytz.utc)
            embed.add_field(
                name="",
                value=f'{format_dt(utc_time, "f")} ({format_dt(utc_time, "R")})',
                inline=False,
            )

            if utc_time < dt.now(pytz.utc).replace(tzinfo=pytz.utc):
                embed.color = 0xFF0000
            if utc_time > dt.now(pytz.utc).replace(tzinfo=pytz.utc):
                embed.color = 0x00FF00

        return embed
