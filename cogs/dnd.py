import json
import os

import requests
import mysql.connector
import dateparser as dp
from dateparser.search import search_dates
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ui import Button, View
from nextcord.abc import GuildChannel
import re

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class DnD(commands.Cog, name="dnd"):
    def __init__(self, bot):
        self.bot = bot

    def remove_tags(self, text):
        cleantext = re.sub(CLEANR, '', text)
        return cleantext

    def generate_embed(self, res, index, max_index):
        embed = nextcord.Embed(
            title=res["results"][index]["name"],
            color=config["success"]
        )
        for key in res["results"][index]:
            if key in ["name", "document_slug", "document_title", "route", "slug", "highlighted"]:
                continue
            value = res["results"][index][key]
            if len(value) == 0:
                continue
            if len(value) > 1000:
                value = value[:1000] + "..."
            embed.add_field(
                name=key,
                value=value,
                inline=False
            )
        embed.set_footer(
            text=f"{index+1}/{max_index}"
        )
        return embed

    @nextcord.slash_command(name="dndsearch", description="Search the D&D 5e SRD")
    async def dndsearch(self, interaction: Interaction, terms: str = SlashOption(description="A query about dnd", required=True)):
        res = json.loads(requests.get(f"https://api.open5e.com/search/?text={terms}").text)
        count = res["count"]
        self.currIndex = 0

        for index, r in enumerate(res["results"]):
            if r["name"].lower() == terms.lower():
                self.currIndex = index
                break

        embed = self.generate_embed(res, self.currIndex, count)
        previous_button = Button(label="<", style=nextcord.ButtonStyle.red)

        async def previous_callback(interaction):
            # edit the embed to show the previous result
            currEmbed = interaction.message.embeds[0].to_dict()
            index = int(currEmbed["footer"]["text"].split("/")[0]) - 1
            if (index + 1) < 0:
                index = count - 1
            else:
                index = index - 1
            newembed = self.generate_embed(res, index, count)
            await interaction.message.edit(embed=newembed)
        
        next_button = Button(label=">", style=nextcord.ButtonStyle.red)

        async def next_callback(interaction):
            # edit the embed to show the previous result
            currEmbed = interaction.message.embeds[0].to_dict()
            index = int(currEmbed["footer"]["text"].split("/")[0]) - 1
            if (index + 1) >= count:
                index = 0
            else:
                index = index + 1
            newembed = self.generate_embed(res, index, count)
            await interaction.message.edit(embed=newembed)
        
        previous_button.callback = previous_callback
        next_button.callback = next_callback

        view = View(timeout=1000)
        view.add_item(previous_button)
        view.add_item(next_button)

        await interaction.response.send_message(embed=embed, view=view)



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(DnD(bot))