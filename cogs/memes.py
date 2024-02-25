import os
import random
import requests
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, SelectOption
from nextcord.abc import GuildChannel
from nextcord.ui import Button, View, Modal, TextInput, StringSelect
import uwuify
import json
import time


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Memes(commands.Cog, name="memes"):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None
        self.meme_options = dict()
        with open("./resources/emoji-mappings.json", encoding="utf8") as file:
            self.emoji_mappings = json.load(file)

    @nextcord.slash_command(
        name="megamind", description="Make a No B*tches? Megamind meme with custom text"
    )
    async def megamind(
        self,
        interaction: Interaction,
        text: str = SlashOption(description="Text to put on the meme", required=True),
    ):
        """
        [Text] Make a No B*tches? Megamind meme with custom text
        """
        params = {
            "template_id": "370867422",
            "username": "nanosplitter",
            "password": config["imgflip_pass"],
            "text0": text,
        }
        r = requests.post("https://api.imgflip.com/caption_image", params=params)
        await interaction.response.send_message(r.json()["data"]["url"])

    @nextcord.message_command(name="uwu")
    async def uwu(self, interaction: Interaction, message: nextcord.Message):
        """
        Tyuwn a message unto a cyute uwyu message. ( ˊ.ᴗˋ )
        """
        flags = uwuify.SMILEY | uwuify.YU
        await interaction.response.send_message(
            uwuify.uwu(message.content, flags=flags)
        )

    @nextcord.message_command(name="pastafy")
    async def pastafy(self, interaction: Interaction, message: nextcord.Message):
        """
        Turn a message into a pastafied message.
        """

        res = ""
        for word in message.content.split(" "):
            res += word + (
                " " + random.choice(self.emoji_mappings[word.lower()]) + " "
                if word in self.emoji_mappings
                else " "
            )
        await interaction.response.send_message(res)

    @nextcord.slash_command(
        name="emojitype", description="Make a message with letter emojis"
    )
    async def nobitches(
        self,
        interaction: Interaction,
        text: str = SlashOption(description="Message to send", required=True),
    ):
        """
        [Text] Make a message with letter emojis
        """
        emoji_mappings = {
            "a": ":regional_indicator_a:",
            "b": ":regional_indicator_b:",
            "c": ":regional_indicator_c:",
            "d": ":regional_indicator_d:",
            "e": ":regional_indicator_e:",
            "f": ":regional_indicator_f:",
            "g": ":regional_indicator_g:",
            "h": ":regional_indicator_h:",
            "i": ":regional_indicator_i:",
            "j": ":regional_indicator_j:",
            "k": ":regional_indicator_k:",
            "l": ":regional_indicator_l:",
            "m": ":regional_indicator_m:",
            "n": ":regional_indicator_n:",
            "o": ":regional_indicator_o:",
            "p": ":regional_indicator_p:",
            "q": ":regional_indicator_q:",
            "r": ":regional_indicator_r:",
            "s": ":regional_indicator_s:",
            "t": ":regional_indicator_t:",
            "u": ":regional_indicator_u:",
            "v": ":regional_indicator_v:",
            "w": ":regional_indicator_w:",
            "x": ":regional_indicator_x:",
            "y": ":regional_indicator_y:",
            "z": ":regional_indicator_z:",
            " ": "   ",
            "0": ":regional_indicator_zero:",
            "1": ":regional_indicator_one:",
            "2": ":regional_indicator_two:",
            "3": ":regional_indicator_three:",
            "4": ":regional_indicator_four:",
            "5": ":regional_indicator_five:",
            "6": ":regional_indicator_six:",
            "7": ":regional_indicator_seven:",
            "8": ":regional_indicator_eight:",
            "9": ":regional_indicator_nine:",
            "!": ":grey_exclamation:",
            "?": ":grey_question:",
            "#": ":hash:",
            "*": ":asterisk:",
        }

        res = [
            f"{emoji_mappings[letter]}" if letter in emoji_mappings else letter
            for letter in text.lower()
        ]

        await interaction.response.send_message("".join(res))

    class MemeMaker(nextcord.ui.Modal):
        def __init__(self, number_of_boxes, meme):
            super().__init__("Meme Maker")  # Modal title
            self.meme = meme
            self.number_of_boxes = number_of_boxes
            self.text_inputs = []
            for i in range(self.number_of_boxes):
                text_input = TextInput(
                    label=f"Input {i + 1}",
                    placeholder=f"Input {i + 1}",
                    max_length=500,
                    required=False,
                )
                self.text_inputs.append(text_input)
                self.add_item(text_input)

        async def callback(self, interaction: Interaction):
            values = []
            for item in self.text_inputs:
                value = item.value
                if value == "":
                    value = " "
                values.append(value)

            params = {
                "template_id": self.meme["id"],
                "username": "nanosplitter",
                "password": config["imgflip_pass"],
            }
            for i in range(len(values)):
                params[f"boxes[{i}][text]"] = values[i]

            r = requests.post("https://api.imgflip.com/caption_image", params=params)
            if r.status_code != 200 or interaction.user is None:
                await interaction.send("Error making meme")
                return

            member = nextcord.utils.get(
                interaction.guild.members, name=interaction.user.name
            )

            embed = nextcord.Embed()
            embed.set_author(
                name=f"New meme from {interaction.user.nick}",
                icon_url=f"{member.display_avatar.url}",
            )
            embed.set_image(url=r.json()["data"]["url"])
            await interaction.channel.send(embed=embed)

    @nextcord.slash_command(name="meme", description="Make a meme with custom text")
    async def meme(
        self,
        interaction: Interaction,
        search: str = SlashOption(description="What meme to make", required=True),
    ):
        """
        [Text] Make a meme with custom text
        """
        selected_meme = None
        for meme in self.meme_options["memes"]:
            if search.lower() == meme["name"].lower():
                selected_meme = meme

        if selected_meme is None:
            await interaction.response.send_message(
                "No meme found with that name", ephemeral=True
            )
            return

        params = {
            "template_id": selected_meme["id"],
            "username": "nanosplitter",
            "password": config["imgflip_pass"],
        }

        for i in range(selected_meme["box_count"]):
            params[f"boxes[{i}][text]"] = f"input{i + 1}"

        r = requests.post("https://api.imgflip.com/caption_image", params=params)
        if r.status_code == 200:
            make_meme_button = Button(
                label="Make meme!", style=nextcord.ButtonStyle.blurple
            )

            async def make_meme_button_callback(interaction):
                modal = self.MemeMaker(selected_meme["box_count"], selected_meme)

                await interaction.response.send_modal(modal)

            make_meme_button.callback = make_meme_button_callback

            view = View(timeout=None)
            view.add_item(make_meme_button)
            await interaction.response.send_message(
                r.json()["data"]["url"], view=view, ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Error creating meme", ephemeral=True
            )

    @meme.on_autocomplete("search")
    async def meme_autocomplete(self, interaction: Interaction, search: str):
        """
        [Text] Make a meme with custom text
        """
        if (
            "memes" not in self.meme_options.keys()
            or self.meme_options["last_cache"] + 500 < time.time()
        ):
            response = requests.get("https://api.imgflip.com/get_memes")
            self.meme_options["memes"] = response.json()["data"]["memes"]
            self.meme_options["last_cache"] = time.time()

        meme_names = []
        for meme in self.meme_options["memes"]:
            if search.lower() in meme["name"].lower():
                meme_names.append(meme["name"])

        await interaction.response.send_autocomplete(meme_names[:25])


def setup(bot):
    bot.add_cog(Memes(bot))
