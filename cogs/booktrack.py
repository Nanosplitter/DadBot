import nextcord
from models.book import Book
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed, SlashOption
from noncommands.booktrackutils import DeleteButton, FinishButton, EditButton
import pytz
import datetime
from datetime import datetime as dt

import yaml

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Booktrack(commands.Cog, name="booktrack"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="booktrack",
        description="default booktrack command",
        guild_ids=[850473081063211048, 856919397754470420],
    )
    async def booktrack(self, interaction: Interaction):
        pass

    @booktrack.subcommand(description="Start a book")
    async def startbook(
        self,
        interaction: Interaction,
        title: str,
        author: str,
        genre: str,
        type: str,
        chapters: int,
        pages: int,
        photo: Optional[nextcord.Attachment] = SlashOption(
            description="A photo that represents the book, possibly a cover",
            required=False,
        ),
    ):
        await interaction.response.defer()
        if photo:
            photo_url = photo.url
        else:
            photo_url = None

        book = Book.create(
            user_id=str(interaction.user.id),
            title=title,
            author=author,
            genre=genre,
            type=type,
            chapters=chapters,
            pages=pages,
            start_date=dt.now(datetime.UTC).replace(tzinfo=pytz.utc),
            photo_url=photo_url,
        )

        embed = book.make_embed()
        await interaction.followup.send(embed=embed)

    @booktrack.subcommand(description="List your books")
    async def list(self, interaction: Interaction):
        await interaction.response.defer()
        books = Book.select().where(Book.user_id == str(interaction.user.id))

        firstReply = False
        for book in books:
            embed = book.make_embed()

            view = nextcord.ui.View(timeout=None)
            view.add_item(DeleteButton(book.id, book.user_id))
            view.add_item(FinishButton(book.id, book.user_id))
            view.add_item(EditButton(book.id, book.user_id))

            if firstReply is False:
                firstReply = True
                await interaction.followup.send(embed=embed, view=view)
            else:
                await interaction.channel.send(embed=embed, view=view)

        if firstReply is False:
            await interaction.followup.send(
                "You have no books! Use `/booktrack startbook` to start one."
            )


def setup(bot):
    bot.add_cog(Booktrack(bot))
