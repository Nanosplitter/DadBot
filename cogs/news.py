import random
import nextcord
import yaml
from nextcord.ext import commands
import feedparser
from bs4 import BeautifulSoup

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class News(commands.Cog, name="news"):
    def __init__(self, bot):
        self.bot = bot

    def clean_description(self, description: str) -> str:
        raw_description = description.split('[&#8230;]</p>')[0]
        return BeautifulSoup(raw_description, 'html.parser').get_text()

    @nextcord.slash_command(name="goodnews", description="Get some good news")
    async def goodnews(self, context):
        """
        [No Arguments] Get some good news
        """
        
        url = "https://www.goodnewsnetwork.org/category/news/feed/"

        feed = feedparser.parse(url)

        message = f"# News from the Good News Network\n{feed.feed.description}\n\n"

        random_entries = random.sample(feed.entries, 3)
        for entry in random_entries:
            clean_description = self.clean_description(entry.description)
            message += f"**[{entry.title}]({entry.link})**\n> {clean_description}[...]\n\n"
        
        await context.send(message)

def setup(bot):
    bot.add_cog(News(bot))
