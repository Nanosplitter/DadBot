import requests
from nextcord import Embed

class Scooby:
    def __init__(self, bot):
        self.bot = bot
    async def apod(self):
        c = self.bot.get_channel(856919399789625376)
        response = requests.get("https://api.nasa.gov/planetary/apod")
        await c.send(embed=Embed(title="Astronomy Picture of the Day", description=response.json()["explanation"]))
        await c.send(response["hdurl"])
    
    async def praiseFireGator(self):
        c = self.bot.get_channel(856919399789625376)
        await c.send("***PRAISE***")