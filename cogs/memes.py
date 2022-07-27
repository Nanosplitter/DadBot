import os
import random
import requests
import yaml
from nextcord.ext import commands
import uwuify

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Memes(commands.Cog, name="memes"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nobitches")
    async def nobitches(self, context, *text):
        """
        [Text] Make a No Bitches? Megamind meme with custom text
        """
        params = {
            "template_id": "370867422", 
            "username": "nanosplitter", 
            "password": config["imgflip_pass"],
            "text0": " ".join(text),
        }
        r = requests.post("https://api.imgflip.com/caption_image", params=params)
        await context.send(r.json()["data"]["url"])

    @commands.command(name="uwu")
    async def uwu(self, context):
        """
        UwU - Wepwy to a message to make it into an UwU message. ( ͡o ꒳ ͡o )
        """
        message = await context.channel.fetch_message(context.message.reference.message_id)
        flags = uwuify.SMILEY | uwuify.YU
        await context.reply(uwuify.uwu(message.content, flags=flags))
    
    @commands.command(name="pastafy")
    async def pastafy(self, context):
        """
        [No Arguments] Turns any message you reply to into a copypasta.
        """
        try:
            message = await context.channel.fetch_message(context.message.reference.message_id)
            res = ""
            for word in message.content.split(" "):
                res += word + (" " + random.choice(self.emoji_mappings[word.lower()]) + " " if word in self.emoji_mappings else " ")
            await message.reply(res)
        except:
            context.send("Something went wrong, you have to reply to a message for me to pastafy it.")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Memes(bot))
