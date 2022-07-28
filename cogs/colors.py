from curses import color_content
import os
import sys
import yaml
from nextcord.ext import commands
from colour import Color
from nextcord.ui import Button, View
import nextcord
import random

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
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
    
    @commands.command(name="changecolor")
    async def changecolor(self, context, color):
        """
        [ColorHexCode] Allows the user to change the color of their nickname. Only usable in some servers.
        """
        try:
            if context.message.guild.id != 856919397754470420 and context.message.guild.id != 850473081063211048 and context.message.guild.id != 1001665668657193001:
                return
            
            limit = 4
            contrast = self.contrast("#36393f", color)

            if contrast < limit:
                embed = nextcord.Embed(
                    title="Error",
                    description="Color does not have enough contrast. That color has a contrast ratio of: " + str(round(contrast, 4)) + ":1. It needs to be above 4:1.",
                    color=int(color.replace("#", ""), 16)
                )
                await context.send(embed=embed)
                return
            userRoles = context.message.author.roles

            if len(userRoles) > 1:
                topRole = userRoles[-1]
                await topRole.edit(colour=nextcord.Colour(int(color.replace("#", ""), 16)))
                embed = nextcord.Embed(
                    title="Success!",
                    description="Color has been changed! The contrast it has is " + str(round(contrast, 4)) + ":1",
                    color=int(color.replace("#", ""), 16)
                )
                await context.send(embed=embed)
        except:
            embed = nextcord.Embed(
                title="Error",
                description="Something went wrong, make sure you are using a 6 digit hex code. (ex: !changecolor #FFFFFF)",
                color=config["error"]
            )
            await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Colors(bot))
