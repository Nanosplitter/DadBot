from datetime import datetime
from zoneinfo import ZoneInfo
import io
import nextcord
from noncommands.constants import SETTINGS_HINT
from services.apod_service import download_image, fetch_apod, format_apod_message
from services.step_log_service import (
    build_embed_for_server,
    build_step_logger_view,
)
from noncommands.adventofcode_service import create_advent_of_code_messages


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

        post = fetch_apod()
        if post is None:
            self.bot.logger.error("NASA APOD is down")
            for channel in channels:
                await channel.send("NASA APOD is currently down :(")
            return

        text = format_apod_message(post, SETTINGS_HINT)
        if post.image_url:
            downloaded = await download_image(post)
            if downloaded:
                data, filename = downloaded
                for channel in channels:
                    await channel.send(
                        text, file=nextcord.File(io.BytesIO(data), filename)
                    )
                return

        for channel in channels:
            await channel.send(text)
            if post.link_url:
                await channel.send(post.link_url)
        return

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
