import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed
from nextcord.utils import format_dt
import dateparser as dp
from pytz import timezone
import pytz
from datetime import datetime

from models.todo import Todo
from noncommands.reminderutils import DeleteButton, SnoozeButton


class TodoCog(commands.Cog, name="todo"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="todo", description="Create and manage your todo items."
    )
    async def todo(self, interaction: Interaction):
        pass

    @todo.subcommand(description="Create a todo item.")
    async def create(
        self,
        interaction: Interaction,
        what: str = SlashOption(
            description="What you want to be reminded about", required=True
        ),
        when: str = SlashOption(
            description="When you want to be reminded about this",
            default="null",
            required=False,
        ),
        tz: str = SlashOption(
            description="The timezone you want to be reminded in",
            default="EDT",
            required=False,
        ),
    ):

        embed = nextcord.Embed(
            title=f":hammer: New Todo item Created! :hammer:", color=0x00FF00
        )
        embed.add_field(name="What", value=what, inline=False)

        when_dt = None
        if when != "null":
            when_dt = dp.parse(
                when,
                settings={
                    "PREFER_DATES_FROM": "future",
                    "PREFER_DAY_OF_MONTH": "first",
                    "TIMEZONE": tz,
                    "RETURN_AS_TIMEZONE_AWARE": True,
                },
            )
            if when_dt:
                embed.add_field(
                    name="When",
                    value=f'{format_dt(when_dt, "f")} ({format_dt(when_dt, "R")})',
                    inline=False,
                )

        embed.set_footer(text="Run `/todo list` to view your todo items.")
        partialMessage = await interaction.response.send_message(embed=embed)

        fullMessage = await partialMessage.fetch()

        Todo.create(
            who=interaction.user.name,
            who_id=interaction.user.id,
            what=what,
            time=when_dt.astimezone(pytz.utc) if when_dt else None,
            channel=interaction.channel.id,
            message_id=fullMessage.id,
            reminded=0,
        )

    @todo.subcommand(description="List your todo items.")
    async def list(self, interaction: Interaction):
        todo_items = Todo.select().where(Todo.who_id == interaction.user.id)

        firstReply = False
        for item in todo_items:
            embed = item.build_embed()

            view = nextcord.ui.View(timeout=None)
            view.add_item(DeleteButton(item.id, item.who_id))
            view.add_item(SnoozeButton(item.id, item.what, item.who_id))

            if not firstReply:
                firstReply = True
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.channel.send(embed=embed, view=view)

        if not firstReply:
            await interaction.response.send_message("You have no todo items!")


def setup(bot):
    bot.add_cog(TodoCog(bot))
