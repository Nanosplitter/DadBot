import asyncio
import os
import io
import random
import sys
import aiohttp
import aiofiles
import hashlib
import yaml
import requests
import uuid
import inspirobot
import uwuify
import json

import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed

from noncommands.dadroid import dadroid_single


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot
        with open("./resources/emoji-mappings.json", encoding="utf8") as file:
            self.emoji_mappings = json.load(file)

    @nextcord.slash_command(
        name="dadjoke", description="Have Dad tell you one of his classics."
    )
    async def dadjoke(
        self,
        interaction: Interaction,
        searchterm: Optional[str] = SlashOption(
            description="A term to try and find a dadjoke about",
            default="",
            required=False,
        ),
    ):
        """
        [(Optional)SearchTerm] Have Dad tell you one of his classics.
        """
        if searchterm is None:
            searchterm = ""

        url = "https://icanhazdadjoke.com/search?term=" + searchterm
        headers = {"Accept": "application/json"}
        r = requests.get(url, headers=headers)
        json = r.json()
        try:
            await interaction.response.send_message(
                random.choice(json["results"])["joke"]
            )
        except:
            await interaction.response.send_message(
                "I don't think I've heard a good one about that yet. Try something else."
            )

    @nextcord.slash_command(name="xkcd", description="Get an xkcd comic.")
    async def xkcd(
        self,
        interaction: Interaction,
        comicnumber: Optional[int] = SlashOption(
            description="A specific xkcd comic, like '1' to get the first comic",
            default="",
            required=False,
        ),
    ):
        """
        [(Optional)xkcdNumber] Retrieve a random or specific xkcd comic
        """
        r = requests.get("http://xkcd.com/info.0.json")
        comicnumber = comicnumber if comicnumber != "" else str(random.choice(range(1, r.json()["num"])))  # type: ignore

        r = requests.get("http://xkcd.com/" + str(comicnumber) + "/info.0.json")

        try:
            await interaction.response.send_message(r.json()["img"])
        except:
            await interaction.response.send_message(
                "I can't find that xkcd comic, try another."
            )

    @nextcord.slash_command(
        name="apod",
        description="Get the astronomy picture of the day from NASA.",
    )
    async def apod(self, interaction: Interaction):
        """
        Get the NASA picture of the day
        """
        await interaction.response.defer()

        response = requests.get(
            "https://api.nasa.gov/planetary/apod?api_key=hQqgupM0Ghb1OTjjrPkoIDw1EJq6pZQQdgMGBpnb"
        )

        if response.status_code != 200 or len(response.json()) == 0:
            await interaction.channel.send("NASA APOD is currently down :(")
            self.bot.logger.error("NASA APOD is down")
            return

        title = "# APOD - " + response.json()["title"] + "\n"
        explanation = ">>> " + response.json()["explanation"] + "\n"

        url = (
            response.json()["hdurl"]
            if "hdurl" in response.json()
            else response.json()["url"]
        )

        if response.json()["media_type"] == "image":
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        await interaction.followup.send(
                            title + explanation,
                            file=nextcord.File(io.BytesIO(data), "image.png"),
                        )
                        return

        await interaction.followup.send(title + explanation)
        await interaction.channel.send(url)

    @nextcord.slash_command(
        name="iswanted", description="See if someone is on the FBI's most wanted list."
    )
    async def iswanted(
        self,
        interaction: Interaction,
        name: Optional[str] = SlashOption(
            description="The name of the person you want to check", required=True
        ),
    ):
        """
        [SearchTerm] See if someone is on the FBI's most wanted list.
        """
        r = requests.get("https://api.fbi.gov/wanted/v1/list", params={"title": name})

        try:
            url = random.choice(r.json()["items"])["files"][0]["url"]
            if url is None:
                url = ""

            if name is None:
                await interaction.response.send_message(
                    "No one with that name is currently wanted by the FBI"
                )
                return

            await interaction.response.send_message(
                name + " might be wanted by the FBI:\n" + url
            )
        except:
            await interaction.response.send_message(
                "No one with that name is currently wanted by the FBI"
            )

    @nextcord.slash_command(
        name="roastme",
        description="Dad's been around the block a few times, give him a try.",
    )
    async def roastme(self, interaction: Interaction):
        """
        [No Arguments] Dad's been around the block a few times, give him a try.
        """

        url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        r = requests.get(url)
        json = r.json()
        await interaction.response.send_message(json["insult"])

    @nextcord.slash_command(name="eightball", description="Ask any question to dad.")
    async def eight_ball(
        self,
        interaction: Interaction,
        question: Optional[str] = SlashOption(
            description="The question you want to ask dad", required=True
        ),
    ):
        """
        [Question] Ask any question to the bot.
        """
        # Use dadroid_single to get a response from the chat model, but make it funny
        await dadroid_single(
            "You are a bot that acts similar to a magic 8 ball, but your answers are specific to the question. Your goal is to answer the following question. It should be a relatively short, but also funny answer. The answer can be in the positive, negative, or neutral. Make sure your answer is specific to the question. Do not start the answer with 'outlook', and make sure the answer is either yes or no.",
            question,
            first_send_method=interaction.response.send_message,
            send_method=interaction.followup.send,
            response_starter=f"{question}\n >>> "
        )

    @nextcord.slash_command(
        name="bitcoin", description="Get the current price of bitcoin."
    )
    async def bitcoin(self, interaction: Interaction):
        """
        [No Arguments] Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = nextcord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=config["success"],
            )
            await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
