from peewee import *
from services.db_service import get_db
from nextcord import Interaction, Embed, ButtonStyle
from nextcord.ui import Button


class Personality(Model):
    id = AutoField()
    user_id = CharField()
    name = CharField()
    personality = CharField()

    class Meta:
        database = get_db()

    def __str__(self):
        return f"Personality: {self.name} ({self.id})"

    def __repr__(self):
        return f"Personality: {self.name} ({self.id})"

    def make_embed(self):
        embed = Embed(title=self.name)
        embed.add_field(
            name="Personality", value=f"{self.personality[:1024]}", inline=False
        )

        return embed


def get_saved_personalities(user_id):
    return Personality.select().where(Personality.user_id == user_id)


def get_personality(user_id, name):
    return Personality.get_or_none(
        (Personality.user_id == user_id) & (Personality.name == name)
    )


def delete_personality(row_id):
    personality = Personality.get_or_none((Personality.id == row_id))
    if personality is not None:
        personality.delete_instance()
        return True

    return False


class DeleteButton(Button):
    def __init__(self, row_id, user_id):
        super().__init__(style=ButtonStyle.red, label="Delete")
        self.row_id = row_id
        self.user_id = user_id

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "You can't delete someone else's book!", ephemeral=True
            )
            return

        if delete_personality(self.row_id):
            await interaction.response.send_message(
                "Personality deleted.", ephemeral=True
            )
            await interaction.message.delete()
        else:
            await interaction.response.send_message(
                "I couldn't delete that personality.", ephemeral=True
            )
