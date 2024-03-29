from peewee import *
from services.db_service import get_db
from nextcord.utils import format_dt
import pytz
import nextcord


class Book(Model):
    id = AutoField()
    user_id = CharField()
    title = CharField()
    author = CharField()
    genre = CharField()
    type = CharField()
    chapters = IntegerField()
    pages = IntegerField()
    rating = FloatField(null=True)
    start_date = DateTimeField()
    finish_date = DateTimeField(null=True)
    photo_url = CharField(null=True)

    class Meta:
        database = get_db()

    def __str__(self):
        return f"Book: {self.title} by {self.author} ({self.id})"

    def __repr__(self):
        return f"Book: {self.title} by {self.author} ({self.id})"

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def make_embed(self):
        embed = nextcord.Embed(title=f"{self.title} by {self.author}")
        embed.color = 0x000000
        embed.add_field(name="Genre", value=f"{self.genre}", inline=False)
        embed.add_field(name="Type", value=f"{self.type}", inline=False)
        embed.add_field(name="Chapters", value=f"{self.chapters}", inline=False)
        embed.add_field(name="Pages", value=f"{self.pages}", inline=False)

        if self.rating:
            embed.add_field(name="Rating", value=f"{self.rating}", inline=False)

        start_date_aware = self.start_date.replace(tzinfo=pytz.utc)
        embed.add_field(
            name="Start Date",
            value=f"{format_dt(start_date_aware, 'f')} ({format_dt(start_date_aware, 'R')})",
            inline=False,
        )

        if self.finish_date:
            finish_date_aware = self.finish_date.replace(tzinfo=pytz.utc)
            embed.color = 0x00FF00
            embed.add_field(
                name="Finish Date",
                value=f"{format_dt(finish_date_aware, 'f')} ({format_dt(finish_date_aware, 'R')})",
                inline=False,
            )

            read_time = finish_date_aware - start_date_aware
            embed.add_field(
                name="Read Time",
                value=f"{read_time}".replace(", 0:00:00", ""),
                inline=False,
            )

        if self.photo_url:
            embed.set_image(url=self.photo_url)
        return embed
