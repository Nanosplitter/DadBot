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

class Personality:
    def __init__(self, id, user_id, name, personality):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.personality = personality

    def __str__(self):
        return f"Personality: {self.name} ({self.id})"
    
    def __repr__(self):
        return f"Personality: {self.name} ({self.id})"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id
    
    def update_db(self):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("UPDATE personalities SET name = %s, personality = %s WHERE id = %s", (self.name, self.personality, self.id))

        mydb.commit()
        mycursor.close()
        mydb.close()

    def make_embed(self):
        embed = nextcord.Embed(title=f"{self.name}")
        embed.color = 0x000000
        embed.add_field(name="Personality", value=f"{self.personality}", inline=False)
        return embed

    def delete(self):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("DELETE FROM personalities WHERE id = %s", (self.id,))

        mydb.commit()
        mycursor.close()
        mydb.close()

class DeleteButton(nextcord.ui.Button):
    def __init__(self, row_id, user_id):
        super().__init__(style=nextcord.ButtonStyle.red, label="Delete")
        self.row_id = row_id
        self.user_id = user_id

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't delete someone else's book!", ephemeral=True)
            return
        
        personality = Personality(self.row_id, self.user_id, None, None)
        personality.delete()
        await interaction.response.send_message(f"Personality deleted!", ephemeral=True)
        await interaction.message.delete()

