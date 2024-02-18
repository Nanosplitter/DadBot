import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed
from nextcord.ui import Button, TextInput
from nextcord.utils import format_dt
import dateparser as dp
from pytz import timezone
import pytz
from datetime import datetime
import yaml
from noncommands.reminderutils import DeleteButton, SnoozeButton

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Todo(commands.Cog, name="todo"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="todo", description="Create and manage your todo items."
    )
    async def todo(
        self,
        interaction: Interaction,
    ):
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
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True,
        )
        mycursor = mydb.cursor(buffered=True)

        embed = nextcord.Embed(
            title=f":hammer: New Todo item Created! :hammer:", color=0x00FF00
        )
        embed.add_field(name=f"What", value=f"{what}", inline=False)

        time = None

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
            local_utc = when_dt.astimezone(timezone("UTC"))
            embed.add_field(
                name=f"When",
                value=f'{format_dt(local_utc, "f")} ({format_dt(local_utc, "R")})',
                inline=False,
            )
            time = local_utc.strftime("%Y-%m-%d %H:%M:%S")

        embed.set_footer(text=f"Run `/todo list` to view your todo items.")

        partialMessage = await interaction.response.send_message(embed=embed)
        fullMessage = await partialMessage.fetch()

        who = interaction.user.name
        who_id = interaction.user.id
        channel = interaction.channel.id
        message_id = fullMessage.id

        mycursor.execute(
            "INSERT INTO remindme (who, who_id, what, time, channel, message_id, reminded) VALUES (%s, %s, %s, %s, %s, %s, 0)",
            (who, who_id, what, time, channel, message_id),
        )

        mydb.commit()
        mycursor.close()
        mydb.close()

    @todo.subcommand(description="List your todo items.")
    async def list(self, interaction: Interaction):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True,
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute(
            "SELECT * FROM remindme WHERE who_id = %s", (str(interaction.user.id),)
        )

        firstReply = False
        for x in mycursor:
            embed = nextcord.Embed(title=f"{x[3]}")

            time = x[4]

            if time is not None:
                time = time.replace(tzinfo=pytz.utc)
                embed.add_field(
                    name=f"",
                    value=f'{format_dt(time, "f")} ({format_dt(time, "R")})',
                    inline=False,
                )
                if time < datetime.utcnow().replace(tzinfo=pytz.utc):
                    embed.color = 0xFF0000
                if time > datetime.utcnow().replace(tzinfo=pytz.utc):
                    embed.color = 0x00FF00

            view = nextcord.ui.View(timeout=None)

            view.add_item(DeleteButton(x[0], x[2]))
            view.add_item(SnoozeButton(x[0], x[3], x[2]))

            if firstReply == False:
                firstReply = True
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.channel.send(embed=embed, view=view)

        if firstReply == False:
            await interaction.response.send_message("You have no todo items!")

        mycursor.close()
        mydb.close()


def setup(bot):
    bot.add_cog(Todo(bot))
