import datetime
from nextcord import Interaction, Embed
from nextcord.ui import TextInput, View, Button, Modal
import nextcord
from peewee import *

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from models.step_log import StepLog

plt.style.use('dark_background')

class StepLoggerModal(Modal):
    def __init__(self, step_message):
        super().__init__("Log your steps!")
        steps_input = TextInput(
            label="Steps", placeholder=f"10000", max_length=7, required=True
        )
        self.add_item(steps_input)
        self.step_message = step_message

    async def callback(self, interaction: Interaction):
        submit_step_log(
            interaction.guild.id, interaction.user.id, self.children[0].value
        )

        await self.step_message.edit(embed=build_embed_for_server(interaction.guild))

        await interaction.response.send_message(
            f"{interaction.user.mention} logged {int(self.children[0].value):,} steps!"
        )

def get_steps_logged_graph(server_id, user_id):
    # Make a graph using matplotlib with a line graph of the cumulative steps logged by the user with the x-axis being the submit time and the y-axis being the cumulative steps
    server_id = str(server_id)
    user_id = str(user_id)
    step_logs = (
        StepLog.select()
        .where(StepLog.server_id == server_id, StepLog.user_id == user_id)
        .order_by(StepLog.submit_time)
    )

    x = [step.submit_time for step in step_logs]
    y = [step.steps for step in step_logs]

    # Calculate the cumulative sum of steps
    y_cumulative = [sum(y[:i+1]) for i in range(len(y))]

    fig, ax = plt.subplots()
    ax.plot(x, y_cumulative)

    # Format x-axis to scale with time and make it more human-readable
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %d'))
    fig.autofmt_xdate()

    ax.set_xlabel("Submit Time")
    ax.set_ylabel("Cumulative Steps")
    ax.set_title("Cumulative Steps Logged Over Time")

    plt.tight_layout()
    plt.savefig("graph.png")

    return "graph.png"

def build_step_logger_view() -> View:
    view = View(timeout=None)
    button = Button(
        style=nextcord.ButtonStyle.primary,
        label="Log Steps",
    )
    button.callback = step_logger_button_callback

    view.add_item(button)
    return view


async def step_logger_button_callback(interaction: Interaction) -> None:
    step_modal = StepLoggerModal(interaction.message)
    await interaction.response.send_modal(step_modal)


def submit_step_log(server_id, user_id, steps) -> StepLog:
    step_log = StepLog(
        server_id=server_id,
        user_id=user_id,
        steps=steps,
        submit_time=datetime.datetime.now(),
    )
    step_log.save()

    return step_log


def get_steps_leaderboard_for_server(server_id) -> list:
    server_id = str(server_id)
    step_logs = (
        StepLog.select()
        .where(StepLog.server_id == server_id)
        .order_by(StepLog.steps.desc())
    )

    step_totals = {}
    step_numbers = {}
    for step_log in step_logs:
        if step_log.user_id in step_totals:
            step_numbers[step_log.user_id] += 1
            step_totals[step_log.user_id] += step_log.steps
        else:
            step_numbers[step_log.user_id] = 1
            step_totals[step_log.user_id] = step_log.steps

    sorted_step_totals = sorted(
        step_totals.items(), key=lambda item: item[1], reverse=True
    )

    step_logs = []
    for step_total in sorted_step_totals:
        step_log = StepLog(server_id=server_id, user_id=step_total[0], steps=step_total[1])
        step_log.total_steps = step_numbers[step_total[0]]
        step_logs.append(
            step_log
        )

    return step_logs


def get_highest_single_day_step_count(server_id):
    server_id = str(server_id)
    step_log = (
        StepLog.select()
        .where(StepLog.server_id == server_id)
        .order_by(StepLog.steps.desc())
        .first()
    )

    return step_log

def build_embed_for_server(guild) -> Embed:

    leaderboard = get_steps_leaderboard_for_server(guild.id)

    highest_days_logged = max([step_log.total_steps for step_log in leaderboard])

    embed = nextcord.Embed(title="No steps yet!")

    first = True

    for step_log in leaderboard:
        member = guild.get_member(int(step_log.user_id))
        name = member.name

        if first:
            leader_step_count = step_log.steps

            embed = nextcord.Embed(
                title="Step Leaderboard",
                color=member.color,
            )

            embed.set_author(
                name=f"{member.name} is in the lead!",
                icon_url=member.display_avatar.url,
            )

            name = f"🏆 {name}"
            first = False

        diff_text = f"(-{leader_step_count - step_log.steps:,})" if step_log.steps < leader_step_count else ""

        days_behind = highest_days_logged - step_log.total_steps
        days_text = f"{days_behind} day{'s' if days_behind != 1 else ''} behind" if step_log.total_steps < highest_days_logged else "Up to date"

        embed.add_field(
            name=name,
            value=f"{step_log.steps:,} steps {diff_text} | {days_text}",
            inline=False,
        )


    top_single_day = get_highest_single_day_step_count(guild.id)

    if top_single_day is not None:
        top_single_day_member = guild.get_member(int(top_single_day.user_id))

        embed.set_footer(
            text=f"Single day record:\n{top_single_day_member.name} with {top_single_day.steps:,} steps",
            icon_url=top_single_day_member.display_avatar.url,
        )

    return embed
