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

class Book:
    def __init__(self, id, user_id, title, author, genre, type, chapters, pages, rating, start_date, finish_date):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.author = author
        self.genre = genre
        self.type = type
        self.chapters = chapters
        self.pages = pages
        self.rating = rating
        self.start_date = start_date
        self.finish_date = finish_date
    
    def __str__(self):
        return f"Book: {self.title} by {self.author} ({self.id})"
    
    def __repr__(self):
        return f"Book: {self.title} by {self.author} ({self.id})"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id

    def make_embed(self):
        embed = nextcord.Embed(title=f"{self.title} by {self.author}")
        embed.color = 0x000000
        embed.add_field(name="Genre", value=f"{self.genre}", inline=False)
        embed.add_field(name="Type", value=f"{self.type}", inline=False)
        embed.add_field(name="Chapters", value=f"{self.chapters}", inline=False)
        embed.add_field(name="Pages", value=f"{self.pages}", inline=False)
        embed.add_field(name="Rating", value=f"{self.rating}", inline=False)
        # start date using discord's time display
        embed.add_field(name="Start Date", value=f"{format_dt(self.start_date.replace(tzinfo=pytz.utc), 'f')} ({format_dt(self.start_date.replace(tzinfo=pytz.utc), 'R')})", inline=False)
        if self.finish_date:
            embed.color = 0x00ff00
            embed.add_field(name="Finish Date", value=f"{format_dt(self.finish_date.replace(tzinfo=pytz.utc), 'f')} ({format_dt(self.finish_date.replace(tzinfo=pytz.utc), 'R')})", inline=False)
        return embed

class DeleteButton(nextcord.ui.Button):
    def __init__(self, row_id, user_id):
        super().__init__(style=nextcord.ButtonStyle.red, label="Delete")
        self.row_id = row_id
        self.user_id = int(user_id)
    
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't delete someone else's book!", ephemeral=True)
            return
        
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("DELETE FROM booktrack WHERE id = %s", (self.row_id,))

        mydb.commit()
        mycursor.close()
        mydb.close()

        await interaction.response.send_message("Book deleted!", ephemeral=True)

        await interaction.message.delete()

class FinishButton(nextcord.ui.Button):
    def __init__(self, row_id, user_id):
        super().__init__(style=nextcord.ButtonStyle.green, label="Mark as Finished")
        self.row_id = row_id
        self.user_id = int(user_id)
    
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't finish someone else's book!", ephemeral=True)
            return
        
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("UPDATE booktrack SET finish_date = %s WHERE id = %s", (datetime.utcnow().replace(tzinfo=pytz.utc), self.row_id))

        mycursor.execute("SELECT * FROM booktrack WHERE id = %s", (self.row_id,))
        book = Book(*mycursor.fetchone())
        embed = book.make_embed()

        mydb.commit()
        mycursor.close()
        mydb.close()

        await interaction.response.send_message("Book finished!", ephemeral=True)

        await interaction.message.edit(embed=embed)