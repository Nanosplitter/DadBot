import requests
from nextcord import Embed

class Scooby:
    def __init__(self, bot):
        self.bot = bot
        
    async def apod(self):
        c = self.bot.get_channel(856919399789625376)
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=hQqgupM0Ghb1OTjjrPkoIDw1EJq6pZQQdgMGBpnb")
        embed = Embed(title="Astronomy Picture of the Day", description=response.json()["explanation"])
        embed.set_image(url=response.json()["hdurl"])
        await c.send(embed=embed)
    
    async def praiseFireGator(self):
        c = self.bot.get_channel(856919399789625376)
        await c.send("***PRAISE***")
    
    async def logSteps(self):
        c = self.bot.get_channel(1095050641157673021)
        await c.send("Time for someone to run `/logsteps`")