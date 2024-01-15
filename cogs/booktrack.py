import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed
from nextcord.ui import Button, TextInput
from nextcord.utils import format_dt
from noncommands.booktrackutils import Book, DeleteButton, FinishButton, EditButton
import dateparser as dp
from pytz import timezone
import pytz
from datetime import datetime
import yaml

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Booktrack(commands.Cog, name="booktrack"):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="booktrack", description="default booktrack command", guild_ids=[850473081063211048, 856919397754470420])
    async def booktrack(self, interaction: Interaction):
        pass
    
    @booktrack.subcommand(description="Start a book")
    async def startbook(self, interaction: Interaction, title: str, author: str, genre: str, type: str, chapters: int, pages: int, rating: float, photo: nextcord.Attachment):
        photo_url = photo.url
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("INSERT INTO booktrack (user_id, title, author, genre, type, chapters, pages, rating, start_date, photo_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (str(interaction.user.id), title, author, genre, type, chapters, pages, rating, datetime.utcnow().replace(tzinfo=pytz.utc), photo_url))

        book = Book(mycursor.lastrowid, interaction.user.id, title, author, genre, type, chapters, pages, rating, datetime.utcnow().replace(tzinfo=pytz.utc), None, photo_url)
        embed = embed = book.make_embed()

        await interaction.response.send_message(embed=embed)

        mydb.commit()
        mycursor.close()
        mydb.close()
    
    @booktrack.subcommand(description="List your books")
    async def list(self, interaction: Interaction):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT * FROM booktrack WHERE user_id = %s", (str(interaction.user.id),))

        firstReply = False
        for x in mycursor:
            book = Book(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11])
            embed = book.make_embed()
            
            view = nextcord.ui.View(timeout = None)

            view.add_item(DeleteButton(book.id, book.user_id))
            view.add_item(FinishButton(book.id, book.user_id))
            view.add_item(EditButton(book.id, book.user_id))


            if firstReply == False:
                firstReply = True
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.channel.send(embed=embed, view=view)
        
        if firstReply == False:
            await interaction.response.send_message("You have no books!")
        
        mycursor.close()
        mydb.close()
    
def setup(bot):
    bot.add_cog(Booktrack(bot))
