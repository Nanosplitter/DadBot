import mysql.connector
import nextcord
from nextcord import Interaction
from nextcord.ui import TextInput
from nextcord.utils import format_dt
import yaml
import dateparser as dp
from pytz import timezone
import pytz
from datetime import datetime

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Snoozer(nextcord.ui.Modal):
    def __init__(self, row_id, what):
        super().__init__("Snoozer")
        self.row_id = row_id
        self.what = what

        when = TextInput(label="When do you want to be reminded?", placeholder="in 2 hours", max_length=200, required=True)
        self.add_item(when)
    
    async def callback(self, interaction: Interaction):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)

        when = self.children[0].value
        when_dt = dp.parse(when, settings={'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first', 'TIMEZONE': 'EDT', 'RETURN_AS_TIMEZONE_AWARE': True})
        local_utc = when_dt.astimezone(timezone("UTC"))

        embed = nextcord.Embed(title=f"{self.what}")
        embed.add_field(name=f"", value=f'{format_dt(local_utc, "f")} ({format_dt(local_utc, "R")})', inline=False)
        
        time = local_utc.strftime('%Y-%m-%d %H:%M:%S')

        if local_utc < datetime.utcnow().replace(tzinfo=pytz.utc):
            embed.color = 0xff0000
        if local_utc > datetime.utcnow().replace(tzinfo=pytz.utc):
            embed.color = 0x00ff00

        mycursor.execute("UPDATE remindme SET time = %s, reminded = 0 WHERE id = %s", (time, self.row_id))

        await interaction.message.edit(embed=embed)

class DeleteButton(nextcord.ui.Button):
    def __init__(self, row_id, who_id):
        super().__init__(style=nextcord.ButtonStyle.green, label="Done")
        self.row_id = row_id
        self.who_id = int(who_id)
    
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.who_id:
            await interaction.response.send_message("You can't delete someone else's todo!", ephemeral=True)
            return
        
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("DELETE FROM remindme WHERE id = %s", (self.row_id,))
        mydb.commit()
        mycursor.close()
        mydb.close()

        await interaction.message.delete()

class SnoozeButton(nextcord.ui.Button):
    def __init__(self, rowId, what, who_id):
        super().__init__(style=nextcord.ButtonStyle.blurple, label="Snooze")
        self.rowId = rowId
        self.what = what
        self.who_id = int(who_id)
    
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.who_id:
            await interaction.response.send_message("You can't snooze someone else's todo!", ephemeral=True)
            return
        
        modal = Snoozer(self.rowId, self.what)
        
        await interaction.response.send_modal(modal)