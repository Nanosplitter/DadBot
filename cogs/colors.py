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
    
    def generateRandomColor(self):
        """
        Generate random color value
        """
        
        randomColor = hex(random.randint(0, 16777216)) # generate random integer
        randomColor = randomColor[2:]

        if (len(randomColor) < 6):
            randomColor = '0' * (6-len(randomColor)) + randomColor

        randomColor = "#" + randomColor

        return randomColor    

    @commands.command(name="changecolor")
    async def changecolor(self, context, color="random"):
        """
        [Color] Allows the user to change the color of their nickname. Only usable in some servers. Use the argument "random" to generate a random color.
        """
        try:
            async def color_callback(interaction):
                """
                Method to execute when the "new color" button is clicked
                """
                if interaction.user == context.author:  # checks that user interacting with button is command sender
                    while True:
                        randomColor = self.generateRandomColor()
                        contrast = self.contrast("#36393f", randomColor)
                        if contrast > limit:
                            break
                        
                    topRole = userRoles[-1]
                    await topRole.edit(colour=nextcord.Colour(int(randomColor.replace("#", ""), 16)))   # changes top role of user
                    await interaction.message.edit(embed=nextcord.Embed (
                                                        title="Success!",
                                                        description="Color has been changed! The hex value is: " + str(randomColor).upper() + ". The contrast ratio is: " + str(round(contrast, 4)) + ":1",
                                                        color=int(randomColor.replace("#", ""), 16)
                                                    ))

                if context.message.guild.id != 856919397754470420 and context.message.guild.id != 850473081063211048:
                    return
            color_button = Button(label="New Color", style=nextcord.ButtonStyle.blurple)    # creates post-embed button
            
            chosenColor = ""
            limit = 4 # set this to determine the minimum contrast ratio
            userRoles = context.message.author.roles

            if color.lower() == "random":   # if message value after !changecolor is "random"
                while True:
                    randomColor = self.generateRandomColor()
                    contrast = self.contrast("#36393f", randomColor)
                    if contrast > limit:
                        chosenColor = randomColor
                        break

            else:   # if message value after !changecolor is not "random"
                contrast = self.contrast("#36393f", color)
                chosenColor = color
                if contrast < limit:
                    embed = nextcord.Embed(
                        title="Error",
                        description="Color does not have enough contrast. That color has a contrast ratio of: " + str(round(contrast, 4)) + ":1. It needs to be above " + limit + ":1.",
                        color=int(color.replace("#", ""), 16)
                    )
                    await context.send(embed=embed)
                    return
                    
            if len(userRoles) > 1:
                topRole = userRoles[-1]
                await topRole.edit(colour=nextcord.Colour(int(chosenColor.replace("#", ""), 16)))

                embed = nextcord.Embed(
                    title="Success!",
                    description="Color has been changed! The hex value is: " + chosenColor.upper() + ". The contrast ratio is: " + str(round(contrast, 4)) + ":1",
                    color=int(chosenColor.replace("#", ""), 16)
                )

                color_button.callback = color_callback
                view = View(timeout=1000)
                view.add_item(color_button)
                await context.send(embed=embed, view=view)

            else:
                embed = nextcord.Embed(
                    title = "Error!",
                    description = "The user has only one role. Color cannot be changed with this command.",
                    color = config["error"]
                )
                await context.send(embed=embed)
                    
        except Exception as e:
            print(e)
            embed = nextcord.Embed(
                title="Error",
                description="Something went wrong, make sure you are using a 6 digit hex code. (ex: !changecolor #FFFFFF)",
                color=config["error"]
            )
            await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Colors(bot))
