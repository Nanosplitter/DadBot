from collections import defaultdict
import re
import yaml
import sys
import os
import mysql.connector
import random
from nextcord import Thread


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Chat:
    def __init__(self, bot):
        self.bot = bot

    async def respond(self, message) -> None:
        if not isinstance(message.channel, Thread):
            return

        if message.author == self.bot.user or message.author.bot:
            return
        
        thread = message.channel

        


