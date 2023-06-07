import os
import sys
import yaml
from colour import Color
from nextcord.ui import Button, View
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import random


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Colors(commands.Cog, name="colors"):
    def __init__(self, bot):
        self.bot = bot

    def luminance(self, color):
        """
        Calculate the luminance of a color.
        """
        red = Color(color).red
        green = Color(color).green
        blue = Color(color).blue

        red = red / 12.92 if red <= 0.04045 else ((red + 0.055) / 1.055)**2.4
        green = green / 12.92 if green <= 0.04045 else ((green + 0.055) / 1.055)**2.4
        blue = blue / 12.92 if blue <= 0.04045 else ((blue + 0.055) / 1.055)**2.4

        return (0.2126 * red) + (0.7152 * green) + (0.0722 * blue)

    def contrast(self, color1, color2):
        """
        Calculate the contrast between two colors.
        """
        lum1 = self.luminance(color1)
        lum2 = self.luminance(color2)

        return (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)
    
    def rgb2hex(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return "#{:02x}{:02x}{:02x}".format(r,g,b)
    
    def hex2rgb(self, hexcode):
        hexcode = hexcode.lstrip("#")
        return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))

    def similarColors(self, color, delta, loop=6):
        rgb = self.hex2rgb(color)

        colors = []
        deltas = [round(delta / u) for u in (1, 1, 1)]
        for _ in range(loop):
            new_rgb = [random.randint(max(0, x - delta), min(x + delta, 255))
                for x, delta in zip(rgb, deltas)]
            colors.append(new_rgb)

        return [self.rgb2hex(color) for color in colors]
    
    def checkContrastOfColorGroup(self, colorGroup):
        for color in colorGroup:
            if self.contrast("#36393f", color) >= 4:
                return [True, color]
        return [False]
    
    async def changeRoleColor(self, color, role):
        await role.edit(colour=nextcord.Colour(int(color.replace("#", ""), 16)))

    @nextcord.slash_command(name="changecolor", description="change your role color", guild_ids=[856919397754470420, 850473081063211048, 1001665668657193001])
    async def changecolor(self, interaction: Interaction, color: str = SlashOption(description="A color hex code, like '#2B5FB3'", required=True)):
        """
        [ColorHexCode] Allows the user to change the color of their nickname. Only usable in some servers.
        """
        try:
            limit = 4
            contrast = self.contrast("#36393f", color)
            if interaction.user is None:
                await interaction.response.send_message("Sorry, I can't find your user information. Please try again later.")
                return
            
            userRoles = interaction.user.roles # type: ignore

            if contrast < limit:
                embed = nextcord.Embed(
                    title="Error",
                    description="Color does not have enough contrast. That color has a contrast ratio of: " + str(round(contrast, 4)) + ":1. It needs to be above 4:1.",
                    color=int(color.replace("#", ""), 16)
                )

                colorButton = Button(label="Closest Color", style=nextcord.ButtonStyle.blurple)

                async def color_callback(interaction):
                    if interaction.user == interaction.user:  # checks that user interacting with button is command sender
                        delta = 1
                        colors = []
                        
                        contrastRes = [False]
                        
                        while not contrastRes[0]:
                            colors = self.similarColors(color, delta, loop=2)
                            contrastRes = self.checkContrastOfColorGroup(colors)
                            delta += 0.05
                        
                        closestValidColor = contrastRes[1]
                        topRole = userRoles[-1]  
                        await self.changeRoleColor(closestValidColor, topRole)
                        await interaction.message.edit(embed = nextcord.Embed(
                            title="Success!",
                            description=f"Color has been changed to {closestValidColor.upper()}! The contrast it has is " + str(round(self.contrast("#36393f", closestValidColor), 4)) + ":1\nClick the button to try again.", # type: ignore
                            color=int(closestValidColor.replace("#", ""), 16) # type: ignore
                        ))
                
                colorButton.callback = color_callback
                view = View(timeout=1000)
                view.add_item(colorButton)

                await interaction.response.send_message(embed=embed, view=view)
                return

            if len(userRoles) > 1:
                topRole = userRoles[-1]
                await topRole.edit(colour=nextcord.Colour(int(color.replace("#", ""), 16)))
                embed = nextcord.Embed(
                    title="Success!",
                    description="Color has been changed! The contrast it has is " + str(round(contrast, 4)) + ":1",
                    color=int(color.replace("#", ""), 16)
                )
                await interaction.response.send_message(embed=embed)
        except:
            embed = nextcord.Embed(
                title="Error",
                description="Something went wrong, make sure you are using a 6 digit hex code. (ex: !changecolor #FFFFFF)",
                color=config["error"]
            )
            await interaction.response.send_message(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Colors(bot))
