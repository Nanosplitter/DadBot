import nextcord
from noncommands.reminderutils import SnoozeButton
import pytz
from datetime import datetime as dt

from models.todo import Todo  # Adjust the import path as needed


class ReminderLoop:

    async def checkReminders(self, bot):
        due_reminders = Todo.select().where(
            (Todo.time <= dt.now(pytz.utc)) & (Todo.reminded == 0)
        )

        for reminder in due_reminders:
            channel = bot.get_channel(int(reminder.channel))

            if channel is None:
                continue

            if reminder.message_id == "-1":
                await channel.send(
                    f"Hey <@{reminder.who_id}>, you asked me to remind you of this:\n\n{reminder.what}"
                )
                continue

            try:
                msg = await channel.fetch_message(reminder.message_id)
            except:
                continue
            try:
                embed = reminder.build_embed()
                view = nextcord.ui.View()
                view.add_item(SnoozeButton(reminder.id, reminder.what, reminder.who_id))

                await msg.reply(
                    f"Hey <@{reminder.who_id}>, you asked me to remind you of [this]({msg.jump_url}):",
                    embed=embed,
                    view=view,
                )
                break
            except:
                pass

    async def updateOldReminders(self, bot):
        query = Todo.update(reminded=1).where(Todo.time <= dt.now(pytz.utc))
        query.execute()
