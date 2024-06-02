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

        channels = [c1, c2]

        response = requests.get(
            "https://api.nasa.gov/planetary/apod?api_key=hQqgupM0Ghb1OTjjrPkoIDw1EJq6pZQQdgMGBpnb"
        )

        for channel in channels:
            if response.status_code != 200 or len(response.json()) == 0:
                await channel.send("NASA APOD is currently down :(")
                self.bot.logger.error("NASA APOD is down")
                return

            await channel.send("# APOD - " + response.json()["title"])
            await channel.send(">>> " + response.json()["explanation"])

            if "hdurl" in response.json():
                await channel.send(response.json()["hdurl"])
            else:
                await channel.send(response.json()["url"])

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
