import hashlib
import os
import random
import sys
import uuid
import aiofiles
import aiohttp
import nextcord
import requests
import yaml
from nextcord.ext import commands

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class NewPicture(commands.Cog, name="newpicture"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="newperson")
    async def newperson(self, context):
        """
        [No Arguments] Creates a picture of a person that does not exist.(From https://thispersondoesnotexist.com/)
        """
        fileName = str(uuid.uuid1()) + str(random.choice(range(1, 1337))) + ".png"
        await self.save_online_person(fileName)
        file = nextcord.File(fileName, filename="newperson.png")
        await context.send("", file=file)
        os.remove(fileName)

    @commands.command(name="newcat")
    async def newcat(self, context):
        """
        [No Arguments] Creates a picture of a cat that does not exist. (From https://thiscatdoesnotexist.com/)
        """
        fileName = str(uuid.uuid1()) + str(random.choice(range(1, 1337))) + ".png"
        await self.save_online_cat(fileName)
        file = nextcord.File(fileName, filename="newcat.png")
        await context.send("", file=file)
        os.remove(fileName)
    
    @commands.command(name="newdog")
    async def newdog(self, context):
        """
        [No Arguments] Gets a random dog pic from https://random.dog
        """
        url = "https://random.dog/woof.json"
        response = requests.get(url)
        json = response.json()
        await context.reply(json["url"])  
    
    async def get_online_person(self) -> bytes:
        url = "https://thispersondoesnotexist.com/image"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers=headers) as r:
                return await r.read()

    async def save_online_person(self, file: str = None) -> int:
        picture = await self.get_online_person()
        return await self.save_picture(picture, file)
    
    async def get_online_cat(self) -> bytes:
        url = "https://thiscatdoesnotexist.com"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers=headers) as r:
                return await r.read()

    async def save_online_cat(self, file: str = None) -> int:
        picture = await self.get_online_cat()
        return await self.save_picture(picture, file)
    
    async def get_checksum_from_picture(self, picture: bytes, method: str = "md5") -> str:
        """Calculate the checksum of the provided picture, using the desired method.
        Available methods can be fetched using the the algorithms_available function.
        :param picture: picture as bytes
        :param method: hashing method as string (optional, default=md5)
        :return: checksum as string
        """
        h = hashlib.new(method.lower())
        h.update(picture)
        return h.hexdigest()
    
    async def save_picture(self, picture: bytes, file: str = None) -> None:
        """Save a picture to a file.
        The picture must be provided as it content as bytes.
        The filename must be provided as a str with the absolute or relative path where to store it.
        If no filename is provided, a filename will be generated using the MD5 checksum of the picture, with jpeg extension.
        :param picture: picture content as bytes
        :param file: filename as string, relative or absolute path (optional)
        :return: None
        """
        if file is None:
            file = self.get_checksum_from_picture(picture) + ".jpeg"
        async with aiofiles.open(file, "wb") as f:
            await f.write(picture)
    
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(NewPicture(bot))
