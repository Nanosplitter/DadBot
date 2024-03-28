from peewee import *
from services.db_service import get_db
import nextcord


class Birthday(Model):
    id = AutoField()
    author = CharField()
    mention = CharField()
    channel_id = CharField()
    birthday = DateTimeField()

    class Meta:
        database = get_db()

    def __repr__(self) -> str:
        return f"{self.mention}'s birthday is {self.birthday}"

    def __str__(self) -> str:
        return f"{self.mention}'s birthday is {self.birthday}"

    def build_embed(self, member, color):
        if color is not None:
            embed = nextcord.Embed(title="", color=color)
        else:
            embed = nextcord.Embed(title="")

        formatted_string = f"{member.display_name} ({self.author})\n{self.birthday.strftime('%B %d, %Y')}"
        embed.set_author(name=formatted_string, icon_url=member.display_avatar.url)

        return embed
