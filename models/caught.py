from peewee import *
from services.db_service import get_db
import nextcord

class Caught(Model):
    id = AutoField()
    user_id = CharField()
    user = CharField()
    count = IntegerField()

    class Meta:
        database = get_db()
    
    def __repr__(self) -> str:
        return f"Caught {self.user} {self.count} times"
    
    def __str__(self) -> str:
        return f"Caught {self.user} {self.count} times"

    def build_embed(self, member, color):
        if color is not None:
            embed = nextcord.Embed(title="", color=color)
        else:
            embed = nextcord.Embed(title="")
        
        formatted_string = f"{member.display_name} ({self.user.split('#')[0]})\n{self.count:2d} times"
        embed.set_author(name=formatted_string, icon_url=member.display_avatar.url)

        return embed

def get_all_in_server(members):
    ids = [member.id for member in members]

    return Caught.select().where(Caught.user_id.in_(ids)).order_by(Caught.count.desc())