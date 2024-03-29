import requests
from nextcord import Embed
from services.step_log_service import (
    build_embed_for_server,
    build_step_logger_view,
)


class Scooby:
    def __init__(self, bot):
        self.bot = bot

    async def apod(self):
        c1 = self.bot.get_channel(856919399789625376)
        c2 = self.bot.get_channel(1105336042296463432)
        response = requests.get(
            "https://api.nasa.gov/planetary/apod?api_key=hQqgupM0Ghb1OTjjrPkoIDw1EJq6pZQQdgMGBpnb"
        )
        embed = Embed(
            title="Astrophotography Picture of the Day",
            description=response.json()["explanation"],
        )
        embed.set_image(url=response.json()["hdurl"])
        await c1.send(embed=embed)
        await c2.send(embed=embed)

    async def praiseFireGator(self):
        c = self.bot.get_channel(856919399789625376)
        await c.send("***PRAISE***")

    async def log_steps(self):
        c = self.bot.get_channel(1095050641157673021)
        await c.send(
            "# Time to log your steps from yesterday!",
            embed=build_embed_for_server(c.guild),
            view=build_step_logger_view(),
        )
