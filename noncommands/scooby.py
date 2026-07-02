from datetime import datetime
from zoneinfo import ZoneInfo
import aiohttp
import io
import nextcord
from noncommands.constants import SETTINGS_HINT
from services.step_log_service import (
    build_embed_for_server,
    build_step_logger_view,
)
from noncommands.adventofcode_service import create_advent_of_code_messages
from noncommands.apod_service import fetch_apod


class Scooby:
    def __init__(self, bot):
        self.bot = bot

    async def apod(self):
        channels = []
        
        for server_id in self.bot.settings:
            server_settings = self.bot.settings[server_id]
            if server_settings.get("apod_enabled") == "True":
                channel = self.bot.get_channel(int(server_settings["apod_channel"]))
                if channel:
                    channels.append(channel)
            

        apod = await fetch_apod()

        if apod is None:
            self.bot.logger.error("NASA APOD is down")
            for channel in channels:
                await channel.send("NASA APOD is currently down :(")
            return

        title = "# APOD - " + apod["title"] + "\n"
        explanation = ">>> " + apod["explanation"] + "\n"

        url = apod["hdurl"] if "hdurl" in apod else apod["url"]

        if apod["media_type"] == "image":
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        for channel in channels:
                            await channel.send(
                                title + explanation + f"{SETTINGS_HINT}",
                                file=nextcord.File(io.BytesIO(data), "image.png"),
                            )
                        return
        for channel in channels:
            await channel.send(title + explanation)
            await channel.send(url)
            await channel.send(f"{SETTINGS_HINT}")

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
    
    async def advent_of_code(self):
        c = self.bot.get_channel(857453949392388107)
        
        await create_advent_of_code_messages(c, day=datetime.now(ZoneInfo('America/New_York')).day)
