import nextcord
from nextcord import Interaction
from nextcord.ui import TextInput
import dateparser as dp
import pytz

from models.todo import Todo


class Snoozer(nextcord.ui.Modal):
    def __init__(self, row_id, what):
        super().__init__("Snoozer")
        self.row_id = row_id
        self.what = what

        when = TextInput(
            label="When do you want to be reminded?",
            placeholder="in 2 hours",
            max_length=200,
            required=True,
        )
        self.add_item(when)

    async def callback(self, interaction: Interaction):
        when = self.children[0].value
        when_dt = dp.parse(
            when,
            settings={
                "PREFER_DATES_FROM": "future",
                "PREFER_DAY_OF_MONTH": "first",
                "TIMEZONE": "EDT",
                "RETURN_AS_TIMEZONE_AWARE": True,
            },
        )

        todo_item = Todo.get_by_id(self.row_id)
        todo_item.time = when_dt.astimezone(pytz.utc)
        todo_item.reminded = 0
        todo_item.save()

        embed = todo_item.build_embed()

        await interaction.message.edit(embed=embed)


class DeleteButton(nextcord.ui.Button):
    def __init__(self, row_id, who_id):
        super().__init__(style=nextcord.ButtonStyle.green, label="Done")
        self.row_id = row_id
        self.who_id = int(who_id)

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.who_id:
            await interaction.response.send_message(
                "You can't delete someone else's todo!", ephemeral=True
            )
            return

        Todo.delete_by_id(self.row_id)
        await interaction.message.delete()


class SnoozeButton(nextcord.ui.Button):
    def __init__(self, row_id, what, who_id):
        super().__init__(style=nextcord.ButtonStyle.blurple, label="Snooze")
        self.row_id = row_id
        self.what = what
        self.who_id = int(who_id)

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.who_id:
            await interaction.response.send_message(
                "You can't snooze someone else's todo!", ephemeral=True
            )
            return

        modal = Snoozer(self.row_id, self.what)
        await interaction.response.send_modal(modal)
