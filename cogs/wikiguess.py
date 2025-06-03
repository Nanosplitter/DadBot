import yaml
import nextcord
from nextcord.ext import commands
import wikipediaapi
import difflib
import random


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Wikiguess(commands.Cog, name="wikiguess"):
    class WikiGuessModal(nextcord.ui.Modal):
        def __init__(self, article: wikipediaapi.WikipediaPage):
            super().__init__(title="WikiGuess")
            self.article = article
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
                    await interaction.response.send_message(
                        "Incorrect. Try again!", ephemeral=True
                    )

    class WikiGuessView(nextcord.ui.View):
        def __init__(self, article: wikipediaapi.WikipediaPage):
            super().__init__(timeout=None)
            self.article = article

        @nextcord.ui.button(label="Guess", style=nextcord.ButtonStyle.primary)
        async def guess_button(
            self, button: nextcord.ui.Button, interaction: nextcord.Interaction
        ):
            modal = Wikiguess.WikiGuessModal(article=self.article)
            await interaction.response.send_modal(modal)

    def __init__(self, bot):
        self.bot = bot
        self.wiki = wikipediaapi.Wikipedia(
            "DadBot (dadbot@colinwilson.dev)", language="en"
        )

    def get_wiki_article(self):
        featured_category = self.wiki.page("Category:Featured articles")
        members = featured_category.categorymembers
        print(f"Found {len(members)} featured articles.")
        print(members.keys())
        articles = [page for page in members.values() if page.ns == 0]
        if not articles:
            return self.wiki.page(self.wiki.random(pages=1))
        page = random.choice(articles)

        print(f"Selected article: {page.title}")
        return page

    @nextcord.slash_command(name="wikiguess", description="Play wikiguess")
    async def wikiguess(self, interaction: nextcord.Interaction):
        article = self.get_wiki_article()
        categories = self.wiki.categories(article, clshow="!hidden")
        categories = [
            categories[category].title.replace("Category:", "").strip()
            for category in categories
        ]

        message = "# WikiGuess\n\n You will be given a random Wikipedia article's categories. Guess the article by clicking the guess button. The winner will be the first with a correct guess!"
        message += "\n\n**Categories:** \n"
        message += "\n".join(f"- {category}" for category in categories)
        await interaction.response.send_message(
            message,
            view=self.WikiGuessView(article=article),
        )


def setup(bot):
    bot.add_cog(Wikiguess(bot))
