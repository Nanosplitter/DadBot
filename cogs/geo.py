from io import BytesIO
import os
import re
import sys
import aiofiles
from discord import Embed
import requests
import nextcord
import urllib.request
import urllib.parse
import random
import json
from  geopy.geocoders import Nominatim
import haversine as hs
import asyncio

geolocator = Nominatim(user_agent="dad-bot")

import yaml
from nextcord.ext import commands
if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


# Here we name the cog and create a new class for the cog.
class Geo(commands.Cog, name="geo"):
    def __init__(self, bot):
        self.geodata = []
        with open("./resources/geodata.json") as file:
            self.geodata = json.load(file)
        self.bot = bot
    
    async def geoplay(self, context, single=False):
        status = "ZERO_RESULTS"
        loc = None

        # get a random number between 1 and 100
        rand = random.randint(1, 10000)

        rulesEmbed = Embed(title="Welcome to Geo Guesser!", description="You will have one minute to guess the location of the picture. To guess, use ||spoilers|| around your guess as to not show the other players your guess. Just send your guess in this channel! If I can read it, I'll put a ✅ under it and delete it, and if I can't I'll put a ❌. Good luck!")
        await context.send(embed=rulesEmbed)
        while(status == "ZERO_RESULTS" or loc is None):
            location = random.choice(self.geodata)
            city = location["name"]
            country = location["country"]
            r = requests.get(f"https://maps.googleapis.com/maps/api/streetview/metadata?radius=3000&source=outdoor&size=1000x1000&location={ urllib.parse.quote(f'{city},{country}') }&key={ config['maps_api_key'] }")
            loc = geolocator.geocode(f'{city},{country}')
            status = r.json()["status"]

        urllib.request.urlretrieve(f"https://maps.googleapis.com/maps/api/streetview?radius=3000&source=outdoor&size=1000x1000&location={ urllib.parse.quote(f'{city},{country}') }&fov=100&heading=0&pitch=0&key={ config['maps_api_key'] }", f"geo{rand}.jpg")

        await context.send("", file=nextcord.File(f"geo{rand}.jpg"))
        os.remove(f"geo{rand}.jpg")
        
        correctLocation = (loc.latitude, loc.longitude)

        guesses = dict()
        embed = nextcord.Embed(title=f"Guesses will go here!")
        embedMessage = await context.send(embed=embed)

        def check(m):
            if m.author.bot or m.channel != context.channel or not re.search("(\|\|[\S\s]*\|\|)", m.content):
                return
            try:
                guessText = m.content.replace("||", "")
                
                guess = geolocator.geocode(f'{guessText}')
                
                guess = (guess.latitude, guess.longitude)
                distance = hs.haversine(guess,correctLocation, unit=hs.Unit.MILES)
                userRoles = m.author.roles
                color = "white"
                if len(userRoles) > 1:
                    topRole = userRoles[-1]
                    color = str(topRole.color).replace("#", "")
                    color = "0x" + color

                guesses["{}".format(m.author.name)] = (distance, guessText, len(guesses.keys()), color)
                players = sorted(guesses.keys(), key=lambda x: (guesses[x][0], guesses[x][2]))

                newEmbed = nextcord.Embed(title=f"Guesses will go here!")
                for i, author in enumerate(players):
                    newEmbed.add_field(name=i+1, value=f"{author}", inline=True)
                loop = asyncio.get_event_loop()
                loop.create_task(embedMessage.edit(embed=newEmbed))
                loop.create_task(m.add_reaction("✅"))
                loop.create_task(m.delete())
                if single:
                    return True
            except:
                loop = asyncio.get_event_loop()
                loop.create_task(m.add_reaction("❌"))
                return

        try:
            await self.bot.wait_for("message", timeout=60.0, check=check)
        except:
            pass
        newEmbed = nextcord.Embed(title=f"The correct location was {city}, {country}!\n(https://maps.google.com/?q={correctLocation[0]},{correctLocation[1]})")
        players = sorted(guesses.keys(), key=lambda x: (guesses[x][0], guesses[x][2]))

        mapurl = f"https://maps.googleapis.com/maps/api/staticmap?size=640x640&scale=3&markers=color:green%7Clabel:CORRECT%7C{correctLocation[0]},{correctLocation[1]}|"

        for i, author in enumerate(players):
            authorloc = geolocator.geocode(f'{guesses[author][1]}')
            mapurl += f"&markers=size:small%7Ccolor:{guesses[author][3]}%7C{authorloc.latitude},{authorloc.longitude}|"
            newEmbed.add_field(name=i+1, value=f"{author}: {guesses[author][1]} ({round(guesses[author][0], 2)} miles away)\n[maps link](https://maps.google.com/?q={authorloc.latitude},{authorloc.longitude})", inline=True)
        loop = asyncio.get_event_loop()
        loop.create_task(embedMessage.edit(embed=newEmbed))
        await context.send(f"Guessing is done!")

        
        print(f"{mapurl}&key={ config['maps_api_key'] }")
        
        urllib.request.urlretrieve(f"{mapurl}&key={ config['maps_api_key'] }", f"answer{rand}.png")
        await context.send("", file=nextcord.File(f"answer{rand}.png"))
        os.remove(f"answer{rand}.png")

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="geo")
    async def geo(self, context):
        """
        Play a round of geo guesser!
        """
        await self.geoplay(context)
    
    @commands.command(name="geosingle")
    async def geosingle(self, context):
        """
        Play a round of geo guesser by yourself!
        """
        await self.geoplay(context, single=True)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Geo(bot))
