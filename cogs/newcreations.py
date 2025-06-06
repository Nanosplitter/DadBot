import nextcord
import requests
import yaml
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

from noncommands.dadroid import dadroid_single


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class NewCreations(commands.Cog, name="newcreations"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="newdog",
        description="Creates a picture of a dog that does not exist.(From https://random.dog/)",
    )
    async def newdog(self, interaction: Interaction):
        """
        [No Arguments] Gets a random dog pic from https://random.dog
        """
        url = "https://random.dog/woof.json"
        response = requests.get(url)
        json = response.json()
        await interaction.response.send_message(json["url"])

    @nextcord.slash_command(
        name="newword",
        description="Creates a new word that does not exist with an optional definition.",
    )
    async def new_word(
        self,
        interaction: Interaction,
        definition: str = SlashOption(
            description="The definition of the word",
            required=False,
            default="",
        ),
    ):
        await interaction.response.defer()

        personality = """
            Your goal is to create a new word that does not yet exist. You may be provided a definition, if you are provided one, then make the new word for that definition, otherwise make up a new word and the definition yourself. You are to respond with just a dictionary entry for that word, and then an example sentence.
        """

        await dadroid_single(
            personality,
            definition,
            interaction.followup.send,
            interaction.channel.send,
            beef=True,
        )


def setup(bot):
    bot.add_cog(NewCreations(bot))
