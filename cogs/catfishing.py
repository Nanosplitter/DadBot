import yaml
import nextcord
from nextcord.ext import commands
import wikipediaapi


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Wikiguess(commands.Cog, name="wikiguess"):
    class WikiGuessView(nextcord.ui.View):
        def __init__(self, article: wikipediaapi.WikipediaPage):
            super().__init__(timeout=None)
            self.article = article

        @nextcord.ui.button(label="Guess", style=nextcord.ButtonStyle.primary)
        async def guess_button(
            self, button: nextcord.ui.Button, interaction: nextcord.Interaction
        ):
            # Logic for handling the guess button click
            await interaction.response.send_message(
                f"Guess button clicked! Article: {self.article.title}", ephemeral=True
            )

    def __init__(self, bot):
        self.bot = bot
        self.wiki = wikipediaapi.Wikipedia(
            "DadBot (dadbot@colinwilson.dev)", language="en"
        )

    def get_wiki_article(self):
        page = self.wiki.page("Golden retriever")

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
        message += f"\n\n**Categories:** \n"
        message += "\n".join(f"- {category}" for category in categories)
        await interaction.response.send_message(
            message,
            view=self.WikiGuessView(article=article),
        )


def setup(bot):
    bot.add_cog(Wikiguess(bot))
