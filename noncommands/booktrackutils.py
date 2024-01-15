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
    def __init__(self, id, user_id, title, author, genre, type, chapters, pages, rating, start_date, finish_date, photo_url):
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
        self.photo_url = photo_url
    
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

        embed.add_field(name="Start Date", value=f"{format_dt(self.start_date.replace(tzinfo=pytz.utc), 'f')} ({format_dt(self.start_date.replace(tzinfo=pytz.utc), 'R')})", inline=False)
        if self.finish_date:
            embed.color = 0x00ff00
            embed.add_field(name="Finish Date", value=f"{format_dt(self.finish_date.replace(tzinfo=pytz.utc), 'f')} ({format_dt(self.finish_date.replace(tzinfo=pytz.utc), 'R')})", inline=False)
        
        if self.photo_url:
            embed.set_image(url=self.photo_url)
        return embed
    
    def update_db(self):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("UPDATE booktrack SET title = %s, author = %s, genre = %s, type = %s, chapters = %s, pages = %s, rating = %s, start_date = %s, finish_date = %s, photo_url = %s WHERE id = %s", (self.title, self.author, self.genre, self.type, self.chapters, self.pages, self.rating, self.start_date, self.finish_date, self.photo_url, self.id))

        mydb.commit()
        mycursor.close()
        mydb.close()

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

class EditButton(nextcord.ui.Button):
    def __init__(self, row_id, user_id):
        super().__init__(style=nextcord.ButtonStyle.blurple, label="Edit")
        self.row_id = row_id
        self.user_id = int(user_id)
    
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't edit someone else's book!", ephemeral=True)
            return
        
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM booktrack WHERE id = %s", (self.row_id,))
        book = Book(*mycursor.fetchone())

        mydb.commit()
        mycursor.close()
        mydb.close()

        await interaction.response.send_modal(EditView(book))



class EditView(nextcord.ui.Modal):
    def __init__(self, book: Book):
        super().__init__("Edit Book")
        self.row_id = book.id
        self.user_id = int(book.user_id)
        self.book = book

        start = TextInput(label="Start", default_value=str(book.start_date)[:10], max_length=200, required=True)
        self.add_item(start)

        if book.finish_date:
            finish = TextInput(label="Finish", default_value=str(book.finish_date)[:10], max_length=200, required=False)
            self.add_item(finish)
    
    async def callback(self, interaction: Interaction):
        start = self.children[0].value

        if len(self.children) > 1:
            finish = self.children[1].value
        else:
            finish = None
        
        start_dt = dp.parse(start, settings={'PREFER_DATES_FROM': 'past', 'PREFER_DAY_OF_MONTH': 'first', 'TIMEZONE': 'EST', 'RETURN_AS_TIMEZONE_AWARE': True})
        self.book.start_date = start_dt.astimezone(timezone("UTC"))

        if finish:
            finish_dt = dp.parse(finish, settings={'PREFER_DATES_FROM': 'past', 'PREFER_DAY_OF_MONTH': 'first', 'TIMEZONE': 'EST', 'RETURN_AS_TIMEZONE_AWARE': True})
            self.book.finish_date = finish_dt.astimezone(timezone("UTC"))

        self.book.update_db()

        embed = self.book.make_embed()

        await interaction.message.edit(embed=embed)