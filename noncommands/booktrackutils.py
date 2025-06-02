import nextcord
from nextcord import Interaction
from nextcord.ui import TextInput
import yaml
import dateparser as dp
from pytz import timezone
import pytz
from datetime import datetime as dt
from models.book import Book

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class DeleteButton(nextcord.ui.Button):
    def __init__(self, book_id, user_id):
        super().__init__(style=nextcord.ButtonStyle.red, label="Delete")
        self.book_id = book_id
        self.user_id = user_id

    async def callback(self, interaction: nextcord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "You can't delete someone else's book!", ephemeral=True
            )
            return

        book = Book.get(Book.id == self.book_id, Book.user_id == self.user_id)
        book.delete_instance()

        await interaction.response.send_message("Book deleted!", ephemeral=True)
        await interaction.message.delete()


class FinishButton(nextcord.ui.Button):
    def __init__(self, book_id, user_id):
        super().__init__(style=nextcord.ButtonStyle.green, label="Mark as Finished")
        self.book_id = book_id
        self.user_id = user_id

    async def callback(self, interaction: nextcord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "You can't finish someone else's book!", ephemeral=True
            )
            return

        book = Book.get(Book.id == self.book_id, Book.user_id == self.user_id)
        book.finish_date = dt.now(pytz.utc)
        book.save()

        embed = book.make_embed()

        await interaction.response.send_message("Book finished!", ephemeral=True)
        await interaction.message.edit(embed=embed)


class EditButton(nextcord.ui.Button):
    def __init__(self, book_id, user_id):
        super().__init__(style=nextcord.ButtonStyle.blurple, label="Edit")
        self.book_id = book_id
        self.user_id = user_id

    async def callback(self, interaction: nextcord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "You can't edit someone else's book!", ephemeral=True
            )
            return

        book = Book.get(Book.id == self.book_id, Book.user_id == self.user_id)
        await interaction.response.send_modal(EditView(book))


class EditView(nextcord.ui.Modal):
    def __init__(self, book: Book):
        super().__init__("Edit Book")
        self.book = book

        start = TextInput(
            label="Start",
            default_value=str(book.start_date)[:10],
            max_length=200,
            required=True,
        )
        self.add_item(start)

        ratingDefault = str(book.rating) if book.rating else ""

        rating = TextInput(
            label="Rating", default_value=ratingDefault, max_length=200, required=False
        )
        self.add_item(rating)

        if book.finish_date:
            finish = TextInput(
                label="Finish",
                default_value=str(book.finish_date)[:10],
                max_length=200,
                required=False,
            )
            self.add_item(finish)

    async def callback(self, interaction: Interaction):
        start = self.children[0].value
        rating = self.children[1].value

        if len(self.children) > 2:
            finish = self.children[2].value
        else:
            finish = None

        start_dt = dp.parse(
            start,
            settings={
                "PREFER_DATES_FROM": "past",
                "PREFER_DAY_OF_MONTH": "first",
                "TIMEZONE": "EST",
                "RETURN_AS_TIMEZONE_AWARE": True,
            },
        )

        if start != str(self.book.start_date)[:10]:
            self.book.start_date = start_dt.astimezone(timezone("UTC"))

        if finish:
            finish_dt = dp.parse(
                finish,
                settings={
                    "PREFER_DATES_FROM": "past",
                    "PREFER_DAY_OF_MONTH": "first",
                    "TIMEZONE": "EST",
                    "RETURN_AS_TIMEZONE_AWARE": True,
                },
            )
            if finish != str(self.book.finish_date)[:10]:
                self.book.finish_date = finish_dt.astimezone(timezone("UTC"))

        self.book.rating = rating if rating else None
        self.book.save()

        embed = self.book.make_embed()
        await interaction.message.edit(embed=embed)
