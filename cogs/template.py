import yaml
import nextcord
from nextcord.ext import commands


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Template(commands.Cog, name="template"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="template", description="This is a testing command that does nothing."
    )
    async def testcommand(self, context):
        """
        [No Arguments] This is a testing command that does nothing.
        """
        await context.send("I'll tell you when you're older. Move along now, child.")


def setup(bot):
    bot.add_cog(Template(bot))
