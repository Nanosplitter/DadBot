from nextcord import Embed
import requests
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import random
import asyncio


import yaml

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

HANGMANPICS = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


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

    @nextcord.slash_command(name="hangman", description="Play a round of hangman!")
    async def hangman(
        self,
        interaction: Interaction,
        word: Optional[str] = SlashOption(
            description="The word to guess.", required=False
        ),
    ):
        """
        [No Arguments] Play a round of hangman!
        """
        guessed = []

        def check(m):
            loop = asyncio.get_event_loop()
            if m.author.bot or m.channel != interaction.channel or len(m.content) != 1:
                return

            if not m.content.lower().isalpha():
                loop.create_task(m.add_reaction("❌"))
                return

            guessed.append(m.content.lower())

            if msg is None:
                return

            loop.create_task(msg.edit(content=self.buildMessage(answer, guessed)))
            loop.create_task(m.delete())

            if all(letter in guessed for letter in answer) or len(
                [i for i in guessed if i not in answer]
            ) == (len(HANGMANPICS) - 1):
                return True

        rulesEmbed = Embed(
            title="Welcome to Hangman!",
            description="You will have 90 seconds to guess the secret word. To guess, just type your letter into this channel. If I can read it, I will delete it and apply it to the game, and if I can't, I'll put a ❌. Good luck!",
        )
        await interaction.response.send_message(embed=rulesEmbed)
        answer = word.lower()
        if answer is None:
            answer = (
                str(random.choice(self.wordList).lower())
                .replace("b'", "")
                .replace("'", "")
            )
        msg = await interaction.followup.send(self.buildMessage(answer, guessed))
        try:
            await self.bot.wait_for("message", timeout=90.0, check=check)
        except:
            pass

        resultEmbed = Embed(
            title="Good try!",
            description="You didn't figure out the secret word! The word was: "
            + answer,
            color=0xFF0000,
        )

        if all(letter in guessed for letter in answer):
            resultEmbed = Embed(
                title="You win!",
                description="You figured out the secret word! The word was: " + answer,
                color=0x00FF00,
            )

        await interaction.followup.send(embed=resultEmbed)


def setup(bot):
    bot.add_cog(Hangman(bot))
