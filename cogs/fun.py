import asyncio
import os
import random
import sys
import aiohttp
import aiofiles
import hashlib
import nextcord
import yaml
from nextcord.ext import commands
import requests
import uuid
import inspirobot
import uwuify
import json

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot
        with open("./resources/emoji-mappings.json", encoding="utf8") as file:
            self.emoji_mappings = json.load(file)
    
    @commands.command(name="dadjoke")
    async def dadjoke(self, context, searchTerm="", *args):
        """
        [(Optional)SearchTerm] Have Dad tell you one of his classics.
        """
        url = "https://icanhazdadjoke.com/search?term=" + searchTerm
        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        json = r.json()
        try:
            await context.reply(random.choice(json["results"])["joke"])
        except:
            await context.reply("I don't think I've heard a good one about that yet. Try something else.")
    
    @commands.command(name="xkcd")
    async def xkcd(self, context, search=""):
        """
        [(Optional)xkcdNumber] Retrieve a random or specific xkcd comic, specify a number like "!xkcd 1" to get the first xkcd comic.
        """
        r = requests.get("http://xkcd.com/info.0.json")
        search = search if search != "" else str(random.choice(range(1, r.json()['num'])))

        r = requests.get("http://xkcd.com/" + search + "/info.0.json")

        try:
            await context.reply(r.json()['img'])
        except:
            await context.reply("I can't find that xkcd comic, try another.")
    
    @commands.command(name="iswanted")
    async def iswanted(self, context, *args):
        """
        [SearchTerm] See if someone is on the FBI's most wanted list.
        """
        name = " ".join(args).strip()
        r = requests.get("https://api.fbi.gov/wanted/v1/list", params={"title": name})

        try:
            url = random.choice(r.json()['items'])["files"][0]['url']
            await context.reply(name + " might be wanted by the FBI:\n" + url)
        except:
            await context.reply("No one with that name is currently wanted by the FBI")
    
    @commands.command(name="roastme")
    async def roastme(self, context):
        """
        [No Arguments] Dad's been around the block a few times, give him a try.
        """

        url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        r = requests.get(url)
        json = r.json()
        await context.reply(json["insult"])
    
    @commands.command(name="8ball")
    async def eight_ball(self, context, *args):
        """
        [Question] Ask any question to the bot.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = nextcord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers) - 1)]}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Question asked by: {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        """
        [No Arguments] Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = nextcord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=config["success"]
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
