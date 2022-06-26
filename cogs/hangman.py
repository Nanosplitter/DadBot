from io import BytesIO
import os
import re
import sys
import aiofiles
from nextcord import Embed
import requests
import nextcord
import urllib.request
import urllib.parse
import random
import json
import asyncio


import yaml
from nextcord.ext import commands
if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# Here we name the cog and create a new class for the cog.
class Hangman(commands.Cog, name="hangman"):
    def __init__(self, bot):
        self.bot = bot
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

        response = requests.get(word_site)
        self.wordList = response.content.splitlines()

    def buildMessage(self, word, guessed):
        message = ""
        message += "```\n"
        message += HANGMANPICS[len([i for i in guessed if i not in word])]
        message += "\n\n"
        message += "Guesses: " + " ".join(guessed)
        message += "\n\n"
        message += "Word: "
        for letter in word:
            if letter in guessed:
                message += letter
            else:
                message += "_"
            message += " "
        message += "```"
        return message

    @commands.command(name="hangman")
    async def hangman(self, context):
        """
        Play a round of hangman!
        """
        guessed = []

        def check(m):
            loop = asyncio.get_event_loop()
            if m.author.bot or m.channel != context.channel or len(m.content) != 1:
                return
            
            if not m.content.lower().isalpha():
                loop.create_task(m.add_reaction("❌"))
                return
            
            guessed.append(m.content.lower())
            
            loop.create_task(msg.edit(content=self.buildMessage(answer, guessed)))
            loop.create_task(m.delete())

            if all(letter in guessed for letter in answer) or len([i for i in guessed if i not in answer]) == (len(HANGMANPICS) - 1):
                return True

        rulesEmbed = Embed(title="Welcome to Hangman!", description="You will have 90 seconds to guess the secret word. To guess, just type your letter into this channel. If I can read it, I will delete it and apply it to the game, and if I can't, I'll put a ❌. Good luck!")
        await context.send(embed=rulesEmbed)
        answer = str(random.choice(self.wordList).lower()).replace("b'", "").replace("'", "")
        msg = await context.send(self.buildMessage(answer, guessed))
        try:
            await self.bot.wait_for("message", timeout=90.0, check=check)
        except:
            pass

        resultEmbed = Embed(title="Good try!", description="You didn't figure out the secret word! The word was: " + answer, color=0xff0000)

        if all(letter in guessed for letter in answer):
            resultEmbed = Embed(title="You win!", description="You figured out the secret word! The word was: " + answer, color=0x00ff00)
            
        await context.send(embed=resultEmbed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Hangman(bot))
