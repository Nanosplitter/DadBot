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
                self.view.add_winner(interaction.user)
            else:
                similarity = difflib.SequenceMatcher(
                    None, guess.lower(), answer.lower()
                ).ratio()
                if similarity > 0.7:
                    self.view.add_close_guess(interaction.user, guess)
                self.view.reveal_letter()
            if self.view.winner:
                await self.view.message.edit(
                    content=self.view.build_message(), view=self.view
                )
            else:
                await self.view.message.edit(content=self.view.build_message())

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
                "_" if letter.isalpha() or letter.isdigit() else letter
                for letter in article.title
            ]
            self.revealed_indices = set()
            self.close_guesses = []
            self.winner = None

        def add_winner(self, user: nextcord.User):
            self.winner = user

        def add_close_guess(self, user: nextcord.User, guess: str):
            self.close_guesses.append((user, guess))

        def reveal_letter(self):
            unrevealed = [
                i
                for i, c in enumerate(self.hint)
                if self.hint[i] == "_"
                and (self.article.title[i].isalpha() or self.article.title[i].isdigit())
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
            filtered_categories = filtered_categories[:20]
            message = "# WikiGuess\n\nYou will be given a random Wikipedia article's categories. Guess the article by clicking the guess button. Every wrong guess will reveal more of the answer. The winner will be the first with a correct guess!"
            message += "\n\n**Categories:** \n"
            message += " :white_small_square: ".join(
                f"{category}" for category in filtered_categories
            )

            if self.close_guesses:
                message += "\n\n**Close Guesses:**\n"
                for user, guess in self.close_guesses:
                    message += f"{user.mention}: {guess}\n"

            if self.winner:
                self.clear_items()
                message += f"\n\n**Winner:** {self.winner.mention} 🎉"
                message += (
                    f"\n\n**Article:** [{self.article.title}]({self.article.fullurl})"
                )
            else:
                message += f"\n\n**Hint:** {' '.join(c if c != '_' else '\\_' for c in self.hint)}"

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
        featured_category = self.wiki.page("Category:Featured articles")
        members = featured_category.categorymembers
        articles = [page for page in members.values() if page.ns == 0]

        page = random.choice(articles)

        print(f"Selected article: {page.title}")
        return page

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
