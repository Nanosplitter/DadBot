from io import BytesIO
import io
import os
import re
import sys
import aiofiles
import requests
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, Embed
import urllib.request
import urllib.parse
import random
import json
from geopy.geocoders import Nominatim
import haversine as hs
import asyncio
import pyshorteners
import base64
from nextcord.ui import Button, View, Modal, TextInput, StringSelect


import yaml
from nextcord.ext import commands

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    urlShortener = pyshorteners.Shortener()


# Here we name the cog and create a new class for the cog.
class Chronophoto(commands.Cog, name="chronophoto"):
    def __init__(self, bot):
        self.geodata = []
        with open("./resources/geodata.json") as file:
            self.geodata = json.load(file)
        self.bot = bot
        self.guesses = dict()

    class ChronoSubmitter(nextcord.ui.Modal):
        def __init__(self, message_to_edit, correctYear, outer_instance):
            super().__init__("Chronophoto Guess")  # Modal title
            self.outer_instance = outer_instance
            self.correctYear = correctYear
            outer_instance.message_to_edit = message_to_edit
            text_input = TextInput(
                label="Year", placeholder=f"e.g. 1960", max_length=4, required=True
            )
            self.add_item(text_input)

        async def callback(self, interaction: Interaction):
            guess = self.children[0].value  # type: ignore
            distance = abs(self.correctYear - int(guess))
            name = interaction.user.nick  # type: ignore
            if name is None:
                if interaction.user is None:
                    name = "Unknown"
                else:
                    name = interaction.user.name

            self.outer_instance.guesses["{}".format(name)] = (
                distance,
                guess,
                len(self.outer_instance.guesses.keys()),
            )

            players = sorted(
                self.outer_instance.guesses.keys(),
                key=lambda x: (
                    self.outer_instance.guesses[x][0],
                    self.outer_instance.guesses[x][2],
                ),
            )

            newEmbed = nextcord.Embed(title=f"Guesses will go here!")
            for i, author in enumerate(players):
                newEmbed.add_field(name=i + 1, value=f"{author}", inline=True)
            loop = asyncio.get_event_loop()
            loop.create_task(self.outer_instance.message_to_edit.edit(embed=newEmbed))

    async def chronoplay(self, interaction, single=False):
        self.guesses = dict()
        r = requests.get("https://www.chronophoto.app/badSneakers.txt")

        urls = json.loads(r.text)

        yearString = random.choice(list(urls.keys()))

        correctYear = int(yearString)

        urlYearList = urls[yearString]

        url = "http://" + random.choice(urlYearList)

        pictureData = requests.get(url)

        file = nextcord.File(io.BytesIO(pictureData.content), "image.png")

        rulesEmbed = Embed(
            title="Welcome to Chronophoto!",
            description="The game will end 20 seconds after the last guess. To guess, click the button. All pictures will be taken anytime between 1900 and today. Good luck!",
        )
        rulesEmbed.set_image(url="attachment://image.png")

        await interaction.response.send_message(file=file, embed=rulesEmbed)

        embed = nextcord.Embed(title=f"Guesses will go here!")
        message_to_edit = await interaction.followup.send(embed=embed)

        make_guess_button = Button(
            label="Make guess!", style=nextcord.ButtonStyle.blurple
        )

        async def make_guess_button_callback(interaction):
            modal = self.ChronoSubmitter(message_to_edit, correctYear, self)

            await interaction.response.send_modal(modal)

        make_guess_button.callback = make_guess_button_callback

        async def view_timeout_callback():
            players = sorted(
                self.guesses.keys(),
                key=lambda x: (self.guesses[x][0], self.guesses[x][2]),
            )

            newEmbed = nextcord.Embed(title=f"The correct year was {correctYear}!")
            for i, author in enumerate(players):
                newEmbed.add_field(
                    name=i + 1,
                    value=f"{author}: {self.guesses[author][1]}",
                    inline=True,
                )
            loop = asyncio.get_event_loop()
            loop.create_task(message_to_edit.edit(embed=newEmbed))
            await interaction.followup.send(f"Guessing is done!")

        view = View(timeout=20)
        view.on_timeout = view_timeout_callback
        view.add_item(make_guess_button)

        await interaction.followup.send("Click the button to make a guess!", view=view)

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @nextcord.slash_command(name="chrono", description="Play a round of chronophoto!")
    async def chrono(self, interaction: Interaction):
        """
        [No Arguments] Play a round of Chronophoto!
        """
        await self.chronoplay(interaction)


def setup(bot):
    bot.add_cog(Chronophoto(bot))
