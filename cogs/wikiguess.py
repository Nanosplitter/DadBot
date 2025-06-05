import yaml
import nextcord
from nextcord.ext import commands
import wikipediaapi
import difflib
import random
import requests
import datetime


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Wikiguess(commands.Cog, name="wikiguess"):
    class WikiGuessModal(nextcord.ui.Modal):
        def __init__(
            self, article: wikipediaapi.WikipediaPage, view: "Wikiguess.WikiGuessView"
        ):
            super().__init__(title="WikiGuess")
            self.article = article
            self.view = view
            self.add_item(
                nextcord.ui.TextInput(
                    label="Your Guess", placeholder="Type your guess here"
                )
            )

        async def callback(self, interaction: nextcord.Interaction):
            guess = self.children[0].value
            answer = self.article.title
            if guess.lower() == answer.lower():
                await interaction.response.send_message(
                    "Correct! You guessed the article.", ephemeral=True
                )
            else:
                similarity = difflib.SequenceMatcher(
                    None, guess.lower(), answer.lower()
                ).ratio()
                if similarity > 0.7:
                    await interaction.response.send_message(
                        "Close! You're almost there!", ephemeral=True
                    )
                else:
                    # Reveal a new letter in the hint
                    self.view.reveal_letter()
                    # Edit the original message to show the updated hint
                    await self.view.message.edit(content=self.view.build_message())
                    await interaction.response.send_message(
                        "Incorrect. Try again!", ephemeral=True
                    )

    class WikiGuessView(nextcord.ui.View):
        def __init__(
            self,
            article: wikipediaapi.WikipediaPage,
            categories: list,
            message: nextcord.Message,
        ):
            super().__init__(timeout=None)
            self.article = article
            self.categories = categories
            self.message = message
            self.hint = [
                "\_" if letter.isalpha() else letter for letter in article.title
            ]
            self.revealed_indices = set()

        def reveal_letter(self):
            unrevealed = [
                i
                for i, c in enumerate(self.hint)
                if self.hint[i] == "_" and self.article.title[i].isalpha()
            ]
            if unrevealed:
                idx = random.choice(unrevealed)
                letter_to_reveal = self.article.title[idx]
                for i, char in enumerate(self.article.title):
                    if char.lower() == letter_to_reveal.lower() and self.hint[i] == "_":
                        self.hint[i] = char
                        self.revealed_indices.add(i)

        def build_message(self):
            filtered_categories = [
                category.replace("Category:", "").strip()
                for category in self.categories
            ]
            filtered_categories = [
                category
                for category in filtered_categories
                if category != self.article.title
            ]
            message = "# WikiGuess\n\n You will be given a random Wikipedia article's categories. Guess the article by clicking the guess button. The winner will be the first with a correct guess!"
            message += "\n\n**Categories:** \n"
            message += "\n".join(f"- {category}" for category in filtered_categories)
            message += f"\n\n**Hint:** {' '.join(self.hint)}"
            return message

        @nextcord.ui.button(label="Guess", style=nextcord.ButtonStyle.primary)
        async def guess_button(
            self, button: nextcord.ui.Button, interaction: nextcord.Interaction
        ):
            modal = Wikiguess.WikiGuessModal(article=self.article, view=self)
            await interaction.response.send_modal(modal)

    def __init__(self, bot):
        self.bot = bot
        self.wiki = wikipediaapi.Wikipedia(
            "DadBot (dadbot@colinwilson.dev)", language="en"
        )

    def get_wiki_article(self):
        today = datetime.date.today()
        year = today.year
        month = today.month
        day = today.day
        url = f"https://en.wikipedia.org/api/rest_v1/feed/featured/{year}/{month:02d}/{day:02d}"
        headers = {"User-Agent": "DadBot (dadbot@colinwilson.dev)"}
        response = requests.get(url, headers=headers)
        data = response.json()

        articles = data["mostread"]["articles"]
        pick = random.choice([article.get("title") for article in articles]).replace(
            "_", " "
        )

        self.bot.logger.info(f"Selected featured article: {pick}")

        return self.wiki.page(pick)

    @nextcord.slash_command(name="wikiguess", description="Play wikiguess")
    async def wikiguess(self, interaction: nextcord.Interaction):
        article = self.get_wiki_article()
        categories = self.wiki.categories(article, clshow="!hidden")
        view = self.WikiGuessView(article=article, categories=categories, message=None)
        message = view.build_message()
        await interaction.response.send_message(
            message,
            view=view,
        )

        view.message = await interaction.original_message()


def setup(bot):
    bot.add_cog(Wikiguess(bot))
