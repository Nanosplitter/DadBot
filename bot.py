import asyncio
import os
import platform
import random
import sys
import re
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from noncommands import haikudetector
from noncommands import imchecker
from noncommands import reminderLoop
from noncommands import birthdayLoop
from noncommands import scooby
from noncommands import chat

import nextcord
import yaml
from nextcord import Interaction
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot, Context

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class DadBot(commands.Bot):
    def __init__(self, loggingFormatter, botConfig) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(botConfig["bot_prefix"]), intents=intents, help_command=None)
        self.logger: logging.Logger = loggingFormatter
        self.config: dict = botConfig
        self.super = super()

intents = nextcord.Intents.default().all()

class LoggingFormatter(logging.Formatter):
    black: str = "\x1b[30m"
    red: str = "\x1b[31m"
    green: str = "\x1b[32m"
    yellow: str = "\x1b[33m"
    blue: str = "\x1b[34m"
    gray: str = "\x1b[38m"

    reset: str = "\x1b[0m"
    bold: str = "\x1b[1m"

    COLORS: dict[int, str] = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record) -> str:
        log_color: str = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format: str = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

logger: logging.Logger = logging.getLogger(name="discord_bot")
logger.setLevel(level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

bot = DadBot(loggingFormatter=logger, botConfig=config)

imChecker = imchecker.ImChecker()
reminderChecker = reminderLoop.ReminderLoop()
birthdayChecker = birthdayLoop.BirthdayLoop(bot)
haikuDetector = haikudetector.HaikuDetector()
scooby = scooby.Scooby(bot)
chat = chat.Chat(bot)



# The code in this even is executed when the bot is ready
@bot.event
async def on_ready() -> None:
    if bot.user is None:
        sys.exit("Bot has no user!")
    
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {nextcord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info(f"Servers: {len(bot.guilds)}")
    # list each server name
    for i in bot.guilds:
        bot.logger.info(f" - {i.name}")
    bot.logger.info(f"Users: {len(bot.users)}")
    bot.logger.info("-------------------")
    status_task.start()
    # if config["sync_commands_globally"]:
    #     bot.logger.info("Syncing commands globally...")
    #     await bot.tree.sync()

# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with your mom"]
    await bot.change_presence(activity=nextcord.Game(random.choice(statuses)))

# Removes the default help command of nextcord.py to be able to create our custom help command.
# bot.remove_command("help")

@bot.event
async def on_message(message: nextcord.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return

    if not re.search("(\|\|[\S\s]*\|\|)", message.content):
        await imChecker.checkIm(message)
        await haikuDetector.checkForHaiku(message)
        await chat.respond(message)

    
    await bot.process_commands(message)


@bot.event
async def on_command_completion(context: Context) -> None:
    if context.command is None:
        bot.logger.warning(f"Command is None: {context}")
        return
    full_command_name: str = context.command.qualified_name
    split: list[str] = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )


@bot.event
async def on_command_error(context: Context, error) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = nextcord.Embed(
            description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B,
        )
        await context.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = nextcord.Embed(
            description="You are missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to execute this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = nextcord.Embed(
            description="I am missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to fully perform this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = nextcord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    else:
        raise error

@tasks.loop(seconds=5)
async def checkTimes():
    await reminderChecker.checkReminders(bot)
    await reminderChecker.updateOldReminders(bot)

if __name__ == "__main__":
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")

checkTimes.start()
scheduler = AsyncIOScheduler()
scheduler.add_job(scooby.apod, CronTrigger(hour = "9", minute = "0", second = "0", timezone="EST"))
scheduler.add_job(birthdayChecker.checkBirthdays, CronTrigger(hour = "8", minute = "0", second = "0", timezone="EST"))
scheduler.add_job(scooby.praiseFireGator, CronTrigger(day_of_week="thu", hour = "0", minute = "0", second = "0", timezone="EST"))
scheduler.start()
bot.run(config["token"])
